class Shape:

    def __init__(self, name):
        self.name = name

    def display(self):
        print("Shape:", self.name)


class Circle(Shape):

    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius


class Rectangle(Shape):

    def __init__(self, name, length, width):
        super().__init__(name)
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


# User Input
print("1. Circle")
print("2. Rectangle")

choice = input("Enter your choice: ")

if choice == "1":

    radius = float(input("Enter radius: "))

    circle = Circle("Circle", radius)

    circle.display()
    print("Area:", circle.area())

elif choice == "2":

    length = float(input("Enter length: "))
    width = float(input("Enter width: "))

    rectangle = Rectangle("Rectangle", length, width)

    rectangle.display()
    print("Area:", rectangle.area())

else:
    print("Invalid choice")

    """
1. Circle
2. Rectangle
Enter your choice: 1
Enter radius: 10
Shape: Circle
Area: 314.0

1. Circle
2. Rectangle
Enter your choice: 2
Enter length: 60
Enter width: 50
Shape: Rectangle
Area: 3000.0
"""