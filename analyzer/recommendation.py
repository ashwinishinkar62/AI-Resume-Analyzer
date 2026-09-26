def recommend_projects(target_role):

    recommendations = {
        "Backend Developer":[
            "Employee Management System",
            "Django REST API",
            "Authentication System",
            "E-Commerce Backend",
            "Blog Application"
        ],
        "Frontend Developer":[
            "Portfolio Website",
            "Weather App",
            "React Todo App",
            "E-Commerce UI",
            "Admin Dashboard"
        ],
        "Full Stack Developer":[
            "E-Commerce Website"
            "Hospital Management System",
            "Job Portal",
            "Student Management System",
            "Online Banking System"
        ],
        "Python Developer":[
            "Library Management System"
            "Face Recognition System",
            "Chat Application",
            "File Sharing App",
            "Task Manager"
        ],
        "Data Analyst":[
            "Sales Dashboard"
            "Customer Churn Analysis",
            "IPL Data Analysis",
            "COVID-19 Dashboard",
            "Stock Market Analysis"
        ],
    }
    return recommendations.get(target_role,[])