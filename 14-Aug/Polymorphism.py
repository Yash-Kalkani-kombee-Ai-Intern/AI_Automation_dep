class Shape:

    def area(self):
        print("Area of shape")


class Circle(Shape):

    def area(self):
        radius = float(input("Enter radius: "))
        result = 3.14 * radius * radius
        print("Circle Area:", result)


class Rectangle(Shape):

    def area(self):
        length = float(input("Enter length: "))
        width = float(input("Enter width: "))
        result = length * width
        print("Rectangle Area:", result)


# User Input
print("1. Circle")
print("2. Rectangle")

choice = input("Enter your choice: ")

if choice == "1":
    shape = Circle()

elif choice == "2":
    shape = Rectangle()

else:
    print("Invalid choice")
    shape = None


if shape:
    shape.area()