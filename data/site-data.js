window.SITE_DATA = {
  profile: {
    name: 'Mehmet Akif ÇAKIR',
    role: 'Mechatronics Engineering Student',
    tagline: 'Exploring robotics, embedded systems, software and intelligent engineering solutions.',
    status: 'Currently learning & building',
    university: 'Manisa Celal Bayar University'
  },
  social: {
    github: 'https://github.com/YOUR-USERNAME',
    linkedin: 'https://www.linkedin.com/in/YOUR-LINKEDIN-USERNAME'
  },
  contact: {
    email: 'your-email@example.com'
  },
  cvPath: 'public/cv.pdf'
};

window.SKILLS_DATA = [
  {
    category: 'Programming',
    items: [
      { name: 'C/C++', level: 'Intermediate' },
      { name: 'Arduino', level: 'Intermediate' },
      { name: 'Python', level: 'Familiar' },
      { name: 'JavaScript', level: 'Familiar' }
    ]
  },
  {
    category: 'Engineering',
    items: [
      { name: 'Mechatronics', level: 'Intermediate' },
      { name: 'Robotics', level: 'Familiar' },
      { name: 'Electronics', level: 'Familiar' },
      { name: 'Embedded Systems', level: 'Familiar' },
      { name: 'Automation', level: 'Learning' },
      { name: 'Technical Drawing', level: 'Learning' }
    ]
  },
  {
    category: 'Tools & Technologies',
    items: [
      { name: 'Git', level: 'Familiar' },
      { name: 'GitHub', level: 'Familiar' },
      { name: 'CAD / 3D Design', level: 'Learning' },
      { name: 'AI Tools', level: 'Familiar' }
    ]
  }
];

window.PROJECTS_DATA = [
  {
    id: 'autonomous-egg-collection-robot',
    title: 'Autonomous Egg Collection Robot',
    description: 'Sensor-based robotics concept using Arduino Nano for navigation and egg/object detection. Uses servo-controlled handling logic and embedded decision flow.',
    technologies: ['Arduino Nano', 'Servo Motor', 'Sensors', 'DC Motors', 'EEPROM', 'Embedded C/C++'],
    category: 'Robotics',
    image: 'public/images/projects/egg-robot.svg',
    github: 'https://github.com/YOUR-USERNAME/YOUR-REPOSITORY',
    demo: '#',
    placeholder: false,
    featured: true
  },
  {
    id: 'line-follower-placeholder',
    title: 'Line Follower Platform (Placeholder)',
    description: 'Editable placeholder: Add your actual line follower implementation details and repository link.',
    technologies: ['Arduino', 'IR Sensors', 'Embedded C/C++'],
    category: 'Electronics',
    image: 'public/images/projects/line-follower.svg',
    github: 'https://github.com/YOUR-USERNAME',
    demo: '#',
    placeholder: true
  },
  {
    id: 'engineering-dashboard-placeholder',
    title: 'Engineering Data Dashboard (Placeholder)',
    description: 'Editable placeholder: Document a project where you visualize sensor/process data for engineering decisions.',
    technologies: ['JavaScript', 'Data Visualization', 'GitHub Pages'],
    category: 'Software',
    image: 'public/images/projects/dashboard.svg',
    github: 'https://github.com/YOUR-USERNAME',
    demo: '#',
    placeholder: true
  },
  {
    id: 'cad-design-placeholder',
    title: 'Mechanical CAD Study Series (Placeholder)',
    description: 'Editable placeholder: Add your technical drawing and 3D design studies.',
    technologies: ['CAD', 'Technical Drawing', 'Design Review'],
    category: 'Engineering',
    image: 'public/images/projects/cad-study.svg',
    github: 'https://github.com/YOUR-USERNAME',
    demo: '#',
    placeholder: true
  },
  {
    id: 'embedded-ai-placeholder',
    title: 'Embedded AI Prototype (Placeholder)',
    description: 'Editable placeholder: Add details for an AI-assisted embedded systems prototype when available.',
    technologies: ['Python', 'Embedded Systems', 'AI'],
    category: 'AI',
    image: 'public/images/projects/embedded-ai.svg',
    github: 'https://github.com/YOUR-USERNAME',
    demo: '#',
    placeholder: true
  }
];

window.BLOG_POSTS = [
  {
    slug: 'how-i-started-learning-robotics',
    title: 'How I Started Learning Robotics',
    date: '2026-01-15',
    category: 'Robotics',
    tags: ['Robotics', 'Learning Path', 'Projects'],
    coverImage: 'public/images/blog/robotics-start.svg',
    summary: 'A practical roadmap for beginning robotics with small, repeatable experiments.',
    content: [
      'This placeholder article explains how to start robotics using small milestones, consistent iteration, and project documentation.',
      'Replace this text with your personal experiences, exact hardware choices, and lessons learned.'
    ],
    placeholder: true
  },
  {
    slug: 'arduino-sensors-from-theory-to-practice',
    title: 'Arduino Sensors: From Theory to Practice',
    date: '2026-02-06',
    category: 'Electronics',
    tags: ['Arduino', 'Sensors', 'Embedded'],
    coverImage: 'public/images/blog/arduino-sensors.svg',
    summary: 'Understanding sensor basics and turning them into reliable project behavior.',
    content: [
      'This placeholder article introduces calibration, filtering noise, and validating sensor readings in simple prototypes.',
      'Replace with your own experiments, code snippets, and diagrams.'
    ],
    placeholder: true
  },
  {
    slug: 'what-i-learned-building-line-follower',
    title: 'What I Learned Building a Line Following Robot',
    date: '2026-03-12',
    category: 'Projects',
    tags: ['Robotics', 'Control', 'Arduino'],
    coverImage: 'public/images/blog/line-follower-blog.svg',
    summary: 'Common design mistakes, tuning strategy, and iteration methods for line follower robots.',
    content: [
      'This placeholder article covers balancing mechanics, sensors, and control logic during practical testing.',
      'Replace with your own measurements and project insights.'
    ],
    placeholder: true
  },
  {
    slug: 'introduction-to-embedded-systems',
    title: 'Introduction to Embedded Systems',
    date: '2026-04-04',
    category: 'Mechatronics',
    tags: ['Embedded', 'Microcontrollers', 'Engineering'],
    coverImage: 'public/images/blog/embedded-intro.svg',
    summary: 'A student-friendly guide to thinking in constraints and deterministic behavior.',
    content: [
      'This placeholder article explains real-time considerations, memory limits, and hardware/software interaction.',
      'Replace with your own curriculum-aligned notes and examples.'
    ],
    placeholder: true
  },
  {
    slug: 'github-for-engineering-students',
    title: 'Getting Started with GitHub as an Engineering Student',
    date: '2026-05-20',
    category: 'Programming',
    tags: ['GitHub', 'Version Control', 'Collaboration'],
    coverImage: 'public/images/blog/github-students.svg',
    summary: 'A practical Git and GitHub workflow for student engineering projects.',
    content: [
      'This placeholder article focuses on commit hygiene, branch usage, and portfolio-ready repositories.',
      'Replace with your personal workflow, repository examples, and lessons learned.'
    ],
    placeholder: true
  }
];
