# Conventions
1. The `main` branch is protected because it must contain only working code that is approved and passed all tests
2. When you pick a task you create a new branch named `issue-{issue-number}/{short-description-in-kebab-case` (e.g. `issue-42/styling-login-form`)
4. Everytime you do relevant working stuff you should commit it, especially if you are going to work on a separate thing that is not connected to the current one
5. Your commits must follow this convention:
    - `feat` is for adding a new feature
    - `fix` is for fixing a bug
    - `refactor` is for changing code for performance or convenience purposes (e.g. readability)
    - `chore` is for everything else (writing documentation, formatting, adding tests, cleaning useless code, etc.)
    -  after the category, there should be a `:` announcing the commit description
    -  after the colon, the commit description should consist of short statements describing the changes
    -  each statement should start with a verb conjugated in an imperative way
    -  statements should be separated from themselves with a `;` (e.g. `feat: add join group button; add join alert`)
    -  other examples:
        - `feat: add new button component; add new button components to templates`
        - `fix: add the stop directive to button component to prevent propagation`
        - `refactor: rewrite button component in typescript`
        - `chore: write button documentation`
6. Once you think the task is completed you can make a pull request to the `main` branch
7. The pull request can be merged only if it passes all tests and is approved by 3 members
