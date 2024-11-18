import datetime
import sys
from pathlib import Path

import click
import plotly.graph_objs as go  # type: ignore
import pytz
import requests
from loguru import logger
from plotly.offline import plot  # type: ignore
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).parent
RESULTS_PATH = ROOT_PATH / "results"
RESULTS_PATH.mkdir(exist_ok=True)


class Settings(BaseSettings):
    """Settings class to manage environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    GITHUB_TOKEN: str  # GitHub API token


settings = Settings()  # type: ignore

API_URL = "https://api.github.com/graphql"  # GitHub GraphQL API endpoint
HEADERS = {"Authorization": f"Bearer {settings.GITHUB_TOKEN}"}  # Authorization header


class Issue(BaseModel):
    """Model representing a GitHub Issue."""

    number: int
    title: str
    created_at: datetime.datetime
    closed_at: datetime.datetime | None
    estimate: float = 0.0
    effective: float = 0.0
    milestone: str | None


@click.command()
@click.option(
    "--start-date", required=True, help="Start date of the sprint (YYYY-MM-DD)"
)
@click.option("--end-date", required=True, help="End date of the sprint (YYYY-MM-DD)")
@click.option("--milestone", required=True, help="Milestone title to filter issues by")
@click.option("--org", required=True, help="GitHub organization or username")
@click.option("--project-number", required=True, type=int, help="GitHub project number")
def main(
    start_date: str, end_date: str, milestone: str, org: str, project_number: int
) -> None:
    """
    Main function that orchestrates fetching issues and building the burndown chart.

    Args:
        start_date (str): Start date of the sprint in 'YYYY-MM-DD' format.
        end_date (str): End date of the sprint in 'YYYY-MM-DD' format.
        milestone (str): Milestone title to filter issues.
        org (str): GitHub organization or username.
        project_number (int): GitHub project number.
    """

    # convert dates to datetime objects with timezone
    start_date_dt = (
        datetime.datetime.strptime(start_date, "%Y-%m-%d")
        .replace(tzinfo=pytz.timezone("Europe/Rome"))
        .date()
    )
    end_date_dt = (
        datetime.datetime.strptime(end_date, "%Y-%m-%d")
        .replace(tzinfo=pytz.timezone("Europe/Rome"))
        .date()
    )

    issues = fetch_issues(org, project_number, milestone)

    if not issues:
        logger.info("No issues found for the specified milestone.")
        sys.exit(0)

    build_burndown_chart(issues, start_date_dt, end_date_dt, milestone)


def fetch_issues(org: str, project_number: int, milestone: str) -> list[Issue]:  # noqa: C901
    """
    Fetches issues from a GitHub project that match the given milestone and label.

    Args:
        org (str): GitHub organization or username.
        project_number (int): GitHub project number.
        milestone (str): Milestone title to filter issues.

    Returns:
        list[Issue]: A list of issues matching the criteria.
    """
    issues: list[Issue] = []
    has_next_page = True
    end_cursor = None

    while has_next_page:
        query = build_graphql_query(org, project_number, end_cursor)
        response = requests.post(
            API_URL, json={"query": query}, headers=HEADERS, timeout=30
        )

        if response.status_code != 200:
            logger.error(f"Error querying GitHub API: {response.status_code}")
            logger.error(response.text)
            sys.exit(1)

        data = response.json()

        if "errors" in data:
            logger.error("GraphQL errors occurred:")
            for error in data["errors"]:
                logger.error(error["message"])
            sys.exit(1)

        # extract issues from the response data
        nodes = data["data"]["organization"]["projectV2"]["items"]["nodes"]

        for node in nodes:
            content = node.get("content")
            if content is None:
                continue

            if content["__typename"] == "Issue":
                labels = [label["name"] for label in content["labels"]["nodes"]]
                if "workflow: task" in labels:
                    # filter by milestone
                    issue_milestone = content.get("milestone", {}).get("title")
                    if issue_milestone == milestone:
                        estimate = 0.0
                        effective = 0.0
                        # extract estimate and effective from fieldValues
                        for field_value in node["fieldValues"]["nodes"]:
                            typename = field_value["__typename"]
                            field_name = None
                            if "field" in field_value:
                                field_name = field_value["field"].get("name")

                            if typename == "ProjectV2ItemFieldNumberValue":
                                if field_name == "Estimate":
                                    estimate = field_value.get("number") or 0.0
                                elif field_name == "Effective":
                                    effective = field_value.get("number") or 0.0

                        # parse dates
                        created_at = datetime.datetime.strptime(
                            content["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
                        ).replace(tzinfo=pytz.timezone("Europe/Rome"))
                        closed_at = (
                            datetime.datetime.strptime(
                                content["closedAt"], "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.timezone("Europe/Rome"))
                            if content["closedAt"]
                            else None
                        )

                        issue = Issue(
                            number=content["number"],
                            title=content["title"],
                            created_at=created_at,
                            closed_at=closed_at,
                            estimate=estimate,
                            effective=effective,
                            milestone=issue_milestone,
                        )
                        issues.append(issue)

        # pagination
        page_info = data["data"]["organization"]["projectV2"]["items"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        end_cursor = page_info["endCursor"]

    return issues


def build_graphql_query(org: str, project_number: int, end_cursor: str | None) -> str:
    """
    Builds the GraphQL query for fetching project items.

    Args:
        org (str): GitHub organization or username.
        project_number (int): GitHub project number.
        end_cursor (str | None): Cursor for pagination.

    Returns:
        str: The GraphQL query string.
    """

    after_clause = f', after: "{end_cursor}"' if end_cursor else ""
    return f"""
    query {{
      organization(login: "{org}") {{
        projectV2(number: {project_number}) {{
          items(first: 100{after_clause}) {{
            pageInfo {{
              hasNextPage
              endCursor
            }}
            nodes {{
              content {{
                __typename
                ... on Issue {{
                  id
                  number
                  title
                  createdAt
                  closedAt
                  milestone {{
                    title
                  }}
                  labels(first: 20) {{
                    nodes {{
                      name
                    }}
                  }}
                }}
              }}
              fieldValues(first: 20) {{
                nodes {{
                  __typename
                  ... on ProjectV2ItemFieldNumberValue {{
                    number
                    field {{
                      ... on ProjectV2FieldCommon {{
                        name
                      }}
                    }}
                  }}
                  # Add other field types if necessary
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """


def build_burndown_chart(
    issues: list[Issue],
    start_date: datetime.date,
    end_date: datetime.date,
    milestone: str,
) -> None:
    """
    Builds and saves the burndown chart based on the issues.

    Args:
        issues (list[Issue]): List of issues to include in the chart.
        start_date (datetime.date): Start date of the sprint.
        end_date (datetime.date): End date of the sprint.
        milestone (str): Milestone title.
    """

    date_range = [
        start_date + datetime.timedelta(days=x)
        for x in range((end_date - start_date).days + 1)
    ]

    remaining_estimate_values: list[float] = []
    remaining_effective_values: list[float] = []
    ideal_line: list[float] = []

    # map dates to issues created and closed
    issues_by_created_date: dict[datetime.date, list[Issue]] = {}
    issues_by_closed_date: dict[datetime.date, list[Issue]] = {}
    total_estimate = 0.0  # total estimate up to current date

    for issue in issues:
        created_date = issue.created_at.date()
        if created_date < start_date:
            # include issues created before start date on the start date
            created_date = start_date
        elif created_date > end_date:
            # ignore issues created after end date
            continue
        issues_by_created_date.setdefault(created_date, []).append(issue)

        if issue.closed_at:
            closed_date = issue.closed_at.date()
            if start_date <= closed_date <= end_date:
                issues_by_closed_date.setdefault(closed_date, []).append(issue)

    remaining_estimate = 0.0
    remaining_effective = 0.0

    for _, current_date in enumerate(date_range):
        # add estimates and effectives of issues created on this date
        created_issues_today = issues_by_created_date.get(current_date, [])
        for issue in created_issues_today:
            remaining_estimate += issue.estimate
            remaining_effective += issue.effective
            total_estimate += issue.estimate  # Update total estimate

        # subtract estimates and effectives of issues closed on this date
        closed_issues_today = issues_by_closed_date.get(current_date, [])
        for issue in closed_issues_today:
            remaining_estimate -= issue.estimate
            remaining_effective -= issue.effective

        # record remaining estimates and effectives
        remaining_estimate_values.append(remaining_estimate)
        remaining_effective_values.append(remaining_effective)

        # calculate ideal value
        days_remaining = (end_date - current_date).days
        total_days = (end_date - start_date).days
        ideal_value = (
            total_estimate * (days_remaining / total_days) if total_days > 0 else 0.0
        )
        ideal_line.append(ideal_value)

    fig = go.Figure()

    # ideal burndown line
    fig.add_trace(  # type: ignore
        go.Scatter(
            x=date_range,
            y=ideal_line,
            mode="lines",
            name="Ideal Burndown",
            line={"dash": "dash", "color": "gray"},
        )
    )

    # estimate line
    fig.add_trace(  # type: ignore
        go.Scatter(
            x=date_range,
            y=remaining_estimate_values,
            mode="lines+markers",
            name="Remaining Estimate",
            line={"color": "green"},
        )
    )

    # effective line
    fig.add_trace(  # type: ignore
        go.Scatter(
            x=date_range,
            y=remaining_effective_values,
            mode="lines+markers",
            name="Remaining Effective",
            line={"color": "red"},
        )
    )

    fig.update_layout(  # type: ignore
        title=f"Sprint {milestone[-1]} Burndown Chart ({start_date} - {end_date})",
        xaxis_title="Date",
        yaxis_title="Remaining Work (Story points 1:1 to hours)",
        xaxis={
            "tickformat": "%Y-%m-%d",
            "tickangle": 90,
            "tickmode": "linear",
            "dtick": "D1",
        },
        hovermode="x unified",
    )

    # save as png
    png_result = RESULTS_PATH / f"burndown_sprint{milestone[-1]}.png"
    fig.write_image(str(png_result), format="png")  # type: ignore

    # save as html
    html_result = RESULTS_PATH / f"burndown_sprint{milestone[-1]}.html"
    plot(fig, filename=str(html_result), auto_open=False)


if __name__ == "__main__":
    main()
