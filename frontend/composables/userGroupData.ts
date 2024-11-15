interface UserGroup {
  id: number;
  name: string;
  description: string;
  category: string;
  recentActivity: string;
  enrollmentCount: number;
}

export const userGroupData = (): UserGroup[] => {
  return [
    {
      id: 1,
      name: "Advanced Data Management",
      description:
        "A course focused on managing complex data systems and architectures.",
      category: "Data Science",
      recentActivity: "2 days ago",
      enrollmentCount: 200,
    },
    {
      id: 2,
      name: "Mobile Development",
      description:
        "Learn to build mobile applications for both iOS and Android platforms.",
      category: "Software Development",
      recentActivity: "1 week ago",
      enrollmentCount: 150,
    },
    {
      id: 3,
      name: "Decentralized Systems",
      description:
        "An in-depth look at blockchain, peer-to-peer networks, and decentralized technologies.",
      category: "Computer Science",
      recentActivity: "3 days ago",
      enrollmentCount: 90,
    },
    {
      id: 4,
      name: "Capstone Project",
      description:
        "A final project where students apply their knowledge to a real-world problem.",
      category: "Project",
      recentActivity: "Just now",
      enrollmentCount: 50,
    },
    {
      id: 5,
      name: "Machine Learning",
      description:
        "An introduction to machine learning, artificial intelligence, and neural networks.",
      category: "Data Science",
      recentActivity: "4 days ago",
      enrollmentCount: 75,
    },
    {
      id: 6,
      name: "Web Development",
      description:
        "Learn to build websites using HTML, CSS, JavaScript, and popular frameworks.",
      category: "Software Development",
      recentActivity: "5 days ago",
      enrollmentCount: 100,
    },
    {
      id: 7,
      name: "Cybersecurity",
      description:
        "An overview of cybersecurity concepts, tools, and best practices.",
      category: "Computer Science",
      recentActivity: "6 days ago",
      enrollmentCount: 120,
    },
    {
      id: 8,
      name: "Data Visualization",
      description:
        "A course focused on creating visual representations of data using popular tools.",
      category: "Data Science",
      recentActivity: "1 week ago",
      enrollmentCount: 80,
    },
    {
      id: 9,
      name: "Software Testing",
      description:
        "Learn to test software applications for bugs, errors, and performance issues.",
      category: "Software Development",
      recentActivity: "2 weeks ago",
      enrollmentCount: 60,
    },
    {
      id: 10,
      name: "Operating Systems",
      description:
        "An in-depth look at operating systems, kernels, and system-level programming.",
      category: "Computer Science",
      recentActivity: "3 weeks ago",
      enrollmentCount: 40,
    },
  ];
};
