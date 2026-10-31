class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)

        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)

    def remove_edge(self, u ,v):
        if u in self.adj_list and v in self.adj_list[u]:
            self.adj_list[u].remove(v)

    def list_incoming_adjacent_vertex(self, vertex):
        incoming = []
        for u in self.adj_list:
            if vertex in self.adj_list[u]:
                incoming.append(u)
        return incoming

    def list_outgoing_adjacent_vertex(self, vertex):
        if vertex in self.adj_list:
            return self.adj_list[vertex]
        return []

class Course:
    def __init__(self, course_code, course_name, credit_hours, level, department, lecturer):
        self.course_code = course_code
        self.course_name = course_name
        self.credit_hours = credit_hours
        self.level = level
        self.department = department
        self.lecturer = lecturer

    def __str__(self):
        return (f"[{self.course_code}] {self.course_name}\n"
                f"  - Credits: {self.credit_hours}\n"
                f"  - Level: {self.level}\n"
                f"  - Department: {self.department}\n"
                f"  - Lecturer: {self.lecturer}")

def main():
    degree_graph = Graph()

    course1 = Course("5022CMD", "Advanced Algorithms", 5, "Core", "Computer Science", "Ms. Vimala Doraisamy")
    course2 = Course("5024CMD", "Data Science", 5, "Core", "Computer Science", "Mr. Light Lau")
    course3 = Course("5027CMD", "Web Development", 2, "Elective", "Computer Science", "Ms. Asvhini Subramaniam ")
    course4 = Course("5026CMD", "Software Engineering", 5, "Core", "Software Engineering", "Ms. Thirunageswari Vija Kumaran")
    course5 = Course("MPU3422", "Integrity and Anti-Corruption", 2, "Elective", "Social Studies", "Ms. Asdiah Masran")
    course6 = Course("4001CMD", "Mathematical Skills for Computing Professionals", 4, "Core", "Mathematics", "Ms. Wendy Bong")
    course7 = Course("4004CMD", "Working with Data", 4, "Core", "Computer Science", "Ms. Usha Jayahkudy")
    course8 = Course("4005CMD", "Integrative Project", 8, "Core", "Computer Science", "Ms. Thirunageswari Vija Kumaran")
    course9 = Course("CSC1212", "Data Communications and Networking", 4, "Core", "Computer Science", "Ms. Norashida Sabari")
    course10 = Course("PDC1107", "Self-Development Skills", 3, "Elective", "Social Studies", "Ms Rafidahtul")

    # Assigning all the details of the entire course to a unique identifier which is the course code
    catalog = {
        "5022CMD": course1,
        "5024CMD": course2,
        "5027CMD": course3,
        "5026CMD": course4,
        "MPU3422": course5,
        "4001CMD": course6,
        "4004CMD": course7,
        "4005CMD": course8,
        "CSC1212": course9,
        "PDC1107": course10
    }

    for code in catalog:
        degree_graph.add_vertex(code)

    degree_graph.add_edge("4004CMD", "5024CMD")
    degree_graph.add_edge("4001CMD", "5022CMD")
    degree_graph.add_edge("4005CMD", "5027CMD")
    degree_graph.add_edge("PDC1107", "MPU3422")
    degree_graph.add_edge("CSC1211", "5026CMD")

    print(f"System initialized successfully with {len(catalog)} courses!")

    while True:
        print("\nCollege Courses Prerequisite System")
        print("1 - Display all courses name")
        print("2 - View course details")
        print("3 - View prerequisites for a course")
        print("4 - View postrequisites for a course")
        print("5 - Add new course and details")
        print("6 - Add existing course as prerequisite")
        print("7 - Remove existing course as prerequisite")
        print("8 - Exit")

        try:
            option = int(input("Please choose a number (1-8): "))
        except ValueError:
            print("Invalid input! Please enter a number 1 - 8!")
            continue

        if option == 1:
            print("All Course Names")
            for code, course in catalog.items():
                print(f"[{code}] {course.course_name}")

        elif option == 2:
            course_code = input("Enter course code to view (e.g. CSC101): ").strip().upper()
            if course_code in catalog:
                course = catalog[course_code]

                if course.level == "Core":
                    print("Core Course Profile:")
                    print(f"Course Code: {course.course_code}")
                    print(f"Course Name: {course.course_name}")
                    print(f"Credit Hours: {course.credit_hours}")
                    print(f"Department: {course.department}")
                    print(f"Lecturer Name: {course.lecturer}")
                else:
                    print("Elective Course Profile")
                    print(f"Course Name: {course.course_name}")
            else:
                print("Course not found!")

        elif option == 3:
            course_code = input("Enter course code to check prerequisites for: ").strip().upper()
            if course_code in catalog:
                prerequisite = degree_graph.list_incoming_adjacent_vertex(course_code)
                if prerequisite:
                    print(f"The prerequisite for {course_code}: ")
                    for p in prerequisite:
                        print(f"{p} - {catalog[p].course_name}")
                else:
                    print("This course has no prerequisites!")
            else:
                print("Course not found!")

        elif option == 4:
            course_code = input("Enter course code to check unlocked courses for: ").strip().upper()
            if course_code in catalog:
                unlocked = degree_graph.list_outgoing_adjacent_vertex(course_code)
                if unlocked:
                    print(f"Courses unlocked by {course_code}:")
                    for u in unlocked:
                        print(f"{u} - {catalog[u].course_name}")
                else:
                    print("This course has no postrequisites!")
            else:
                print("Course not found!")

        elif option == 5:
            course_code = input("Enter course code (e.g. CSC101): ").upper()
            course_name = input("Enter course name: ")
            try:
                credit_hours = int(input("Enter credit hours: "))
            except ValueError:
                print("Credit hours must be integer!")
                continue
            level = input("Enter elective: ")
            department = input("Enter department: ")
            lecturer = input("Enter lecturer's name: ")

            new_course = Course(course_code, course_name, credit_hours, level, department, lecturer)
            catalog[course_code] = new_course
            degree_graph.add_vertex(course_code)
            print("Successfully added a new course!")

        elif option == 6:
            prerequisite = input("Enter the prerequisite course (e.g. CSC101): ").strip().upper()
            course = input("Enter the postrequisite course (e.g. CSC101): ").strip().upper()

            if prerequisite in catalog and course in catalog:
                degree_graph.add_edge(prerequisite, course)
                print(f"Successfully connected the {prerequisite} as a prerequisite for {course}!")
            else:
                print("Error occurred! Either one of the courses do not exist!")

        elif option == 7:
            prerequisite = input("Enter the prerequisite course (e.g. CSC101): ").strip().upper()
            course = input("Enter the postrequisite course (e.g. CSC101): ").strip().upper()

            if prerequisite in catalog and course in catalog:
                degree_graph.remove_edge(prerequisite, course)
                print(f"Successfully removed the {prerequisite} as a prerequisite for {course}!")
            else:
                print("Error occurred! Either one of the courses do not exist!")

        elif option == 8:
            print("Exiting...")
            print("Exited!")
            break

if __name__ == "__main__":
    main()