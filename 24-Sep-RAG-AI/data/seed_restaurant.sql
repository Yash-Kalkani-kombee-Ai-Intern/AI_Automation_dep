USE restaurant_ai;

-- ============================================
-- 1. CUSTOMERS - 30 records
-- ============================================

INSERT INTO customers (customer_id, name, email, phone)
VALUES
('C001', 'Yash', 'yash@example.com', '9876543210'),
('C002', 'Rahul', 'rahul@example.com', '9876543211'),
('C003', 'Priya', 'priya@example.com', '9876543212'),
('C004', 'Amit', 'amit@example.com', '9876543213'),
('C005', 'Neha', 'neha@example.com', '9876543214'),
('C006', 'Rohan', 'rohan@example.com', '9876543215'),
('C007', 'Anjali', 'anjali@example.com', '9876543216'),
('C008', 'Vikram', 'vikram@example.com', '9876543217'),
('C009', 'Sneha', 'sneha@example.com', '9876543218'),
('C010', 'Karan', 'karan@example.com', '9876543219'),
('C011', 'Meera', 'meera@example.com', '9876543220'),
('C012', 'Arjun', 'arjun@example.com', '9876543221'),
('C013', 'Pooja', 'pooja@example.com', '9876543222'),
('C014', 'Nikhil', 'nikhil@example.com', '9876543223'),
('C015', 'Kavya', 'kavya@example.com', '9876543224'),
('C016', 'Dev', 'dev@example.com', '9876543225'),
('C017', 'Simran', 'simran@example.com', '9876543226'),
('C018', 'Harsh', 'harsh@example.com', '9876543227'),
('C019', 'Isha', 'isha@example.com', '9876543228'),
('C020', 'Manav', 'manav@example.com', '9876543229'),
('C021', 'Riya', 'riya@example.com', '9876543230'),
('C022', 'Dhruv', 'dhruv@example.com', '9876543231'),
('C023', 'Tanya', 'tanya@example.com', '9876543232'),
('C024', 'Aditya', 'aditya@example.com', '9876543233'),
('C025', 'Sakshi', 'sakshi@example.com', '9876543234'),
('C026', 'Varun', 'varun@example.com', '9876543235'),
('C027', 'Ayesha', 'ayesha@example.com', '9876543236'),
('C028', 'Mohit', 'mohit@example.com', '9876543237'),
('C029', 'Naina', 'naina@example.com', '9876543238'),
('C030', 'Raj', 'raj@example.com', '9876543239');


-- ============================================
-- 2. RESTAURANT TABLES - 25 records
-- ============================================

INSERT INTO restaurant_tables
(table_id, table_number, capacity, location, status)
VALUES
('T01', 1, 2, 'Window', 'available'),
('T02', 2, 2, 'Window', 'reserved'),
('T03', 3, 4, 'Indoor', 'available'),
('T04', 4, 4, 'Indoor', 'occupied'),
('T05', 5, 6, 'Garden', 'available'),
('T06', 6, 2, 'Window', 'available'),
('T07', 7, 4, 'Indoor', 'reserved'),
('T08', 8, 6, 'Garden', 'occupied'),
('T09', 9, 2, 'Window', 'available'),
('T10', 10, 4, 'Indoor', 'available'),
('T11', 11, 8, 'Private', 'reserved'),
('T12', 12, 2, 'Window', 'available'),
('T13', 13, 4, 'Indoor', 'occupied'),
('T14', 14, 6, 'Garden', 'available'),
('T15', 15, 8, 'Private', 'available'),
('T16', 16, 2, 'Window', 'reserved'),
('T17', 17, 4, 'Indoor', 'available'),
('T18', 18, 6, 'Garden', 'occupied'),
('T19', 19, 2, 'Window', 'available'),
('T20', 20, 4, 'Indoor', 'reserved'),
('T21', 21, 8, 'Private', 'available'),
('T22', 22, 6, 'Garden', 'available'),
('T23', 23, 2, 'Window', 'occupied'),
('T24', 24, 4, 'Indoor', 'available'),
('T25', 25, 6, 'Garden', 'reserved');


-- ============================================
-- 3. MENU ITEMS - 30 records
-- ============================================

INSERT INTO menu_items
(item_id, name, category, price, available)
VALUES
('M001', 'Margherita Pizza', 'Pizza', 350.00, TRUE),
('M002', 'Farmhouse Pizza', 'Pizza', 450.00, TRUE),
('M003', 'Paneer Pizza', 'Pizza', 420.00, TRUE),
('M004', 'Pasta Alfredo', 'Pasta', 280.00, TRUE),
('M005', 'Arrabbiata Pasta', 'Pasta', 260.00, TRUE),
('M006', 'Veg Burger', 'Burger', 220.00, TRUE),
('M007', 'Cheese Burger', 'Burger', 280.00, TRUE),
('M008', 'Paneer Burger', 'Burger', 300.00, TRUE),
('M009', 'Paneer Tikka', 'Starter', 300.00, TRUE),
('M010', 'Veg Spring Rolls', 'Starter', 220.00, TRUE),
('M011', 'French Fries', 'Starter', 150.00, TRUE),
('M012', 'Garlic Bread', 'Starter', 180.00, TRUE),
('M013', 'Masala Dosa', 'Main Course', 200.00, TRUE),
('M014', 'Paneer Biryani', 'Main Course', 320.00, TRUE),
('M015', 'Veg Biryani', 'Main Course', 280.00, TRUE),
('M016', 'Dal Makhani', 'Main Course', 250.00, TRUE),
('M017', 'Butter Naan', 'Bread', 80.00, TRUE),
('M018', 'Cheese Naan', 'Bread', 140.00, TRUE),
('M019', 'Tandoori Roti', 'Bread', 50.00, TRUE),
('M020', 'Plain Rice', 'Rice', 120.00, TRUE),
('M021', 'Jeera Rice', 'Rice', 160.00, TRUE),
('M022', 'Cold Coffee', 'Beverage', 120.00, TRUE),
('M023', 'Fresh Lime Soda', 'Beverage', 100.00, TRUE),
('M024', 'Mango Shake', 'Beverage', 180.00, TRUE),
('M025', 'Masala Chai', 'Beverage', 70.00, TRUE),
('M026', 'Chocolate Brownie', 'Dessert', 180.00, TRUE),
('M027', 'Gulab Jamun', 'Dessert', 140.00, TRUE),
('M028', 'Ice Cream', 'Dessert', 150.00, TRUE),
('M029', 'Cheesecake', 'Dessert', 250.00, TRUE),
('M030', 'Fruit Salad', 'Dessert', 180.00, FALSE);


-- ============================================
-- 4. RESERVATIONS - 30 records
-- ============================================

INSERT INTO reservations
(reservation_id, customer_id, table_id, reservation_date, reservation_time, guests, status)
VALUES
('R101', 'C001', 'T01', '2026-09-24', '19:00:00', 2, 'confirmed'),
('R102', 'C002', 'T02', '2026-09-24', '20:00:00', 2, 'confirmed'),
('R103', 'C003', 'T03', '2026-09-24', '19:30:00', 3, 'confirmed'),
('R104', 'C004', 'T05', '2026-09-25', '20:30:00', 5, 'confirmed'),
('R105', 'C005', 'T07', '2026-09-25', '18:30:00', 4, 'pending'),
('R106', 'C006', 'T10', '2026-09-25', '19:00:00', 3, 'confirmed'),
('R107', 'C007', 'T11', '2026-09-25', '21:00:00', 7, 'confirmed'),
('R108', 'C008', 'T14', '2026-09-26', '20:00:00', 5, 'confirmed'),
('R109', 'C009', 'T15', '2026-09-26', '21:00:00', 8, 'confirmed'),
('R110', 'C010', 'T16', '2026-09-26', '18:00:00', 2, 'cancelled'),
('R111', 'C011', 'T17', '2026-09-26', '19:30:00', 4, 'confirmed'),
('R112', 'C012', 'T18', '2026-09-27', '20:30:00', 6, 'pending'),
('R113', 'C013', 'T20', '2026-09-27', '19:00:00', 4, 'confirmed'),
('R114', 'C014', 'T21', '2026-09-27', '21:00:00', 8, 'confirmed'),
('R115', 'C015', 'T22', '2026-09-28', '18:30:00', 5, 'confirmed'),
('R116', 'C016', 'T23', '2026-09-28', '19:00:00', 2, 'cancelled'),
('R117', 'C017', 'T24', '2026-09-28', '20:00:00', 4, 'confirmed'),
('R118', 'C018', 'T25', '2026-09-28', '21:00:00', 6, 'confirmed'),
('R119', 'C019', 'T03', '2026-09-29', '19:30:00', 3, 'pending'),
('R120', 'C020', 'T04', '2026-09-29', '20:00:00', 4, 'confirmed'),
('R121', 'C021', 'T05', '2026-09-29', '21:00:00', 5, 'confirmed'),
('R122', 'C022', 'T08', '2026-09-30', '19:00:00', 6, 'confirmed'),
('R123', 'C023', 'T09', '2026-09-30', '18:30:00', 2, 'confirmed'),
('R124', 'C024', 'T12', '2026-09-30', '20:30:00', 2, 'pending'),
('R125', 'C025', 'T13', '2026-10-01', '19:30:00', 4, 'confirmed'),
('R126', 'C026', 'T14', '2026-10-01', '20:00:00', 5, 'confirmed'),
('R127', 'C027', 'T15', '2026-10-01', '21:00:00', 7, 'confirmed'),
('R128', 'C028', 'T17', '2026-10-02', '19:00:00', 4, 'confirmed'),
('R129', 'C029', 'T19', '2026-10-02', '20:30:00', 2, 'cancelled'),
('R130', 'C030', 'T20', '2026-10-02', '21:00:00', 4, 'confirmed');


-- ============================================
-- 5. ORDERS - 30 records
-- ============================================

INSERT INTO orders
(order_id, customer_id, item_id, quantity, order_date, status)
VALUES
('O001', 'C001', 'M001', 1, '2026-09-24 19:30:00', 'completed'),
('O002', 'C001', 'M022', 2, '2026-09-24 19:35:00', 'completed'),
('O003', 'C002', 'M004', 1, '2026-09-24 20:20:00', 'completed'),
('O004', 'C002', 'M011', 2, '2026-09-24 20:25:00', 'completed'),
('O005', 'C003', 'M009', 1, '2026-09-24 19:50:00', 'completed'),
('O006', 'C004', 'M014', 2, '2026-09-25 20:45:00', 'pending'),
('O007', 'C005', 'M006', 1, '2026-09-25 18:50:00', 'completed'),
('O008', 'C005', 'M026', 2, '2026-09-25 19:00:00', 'completed'),
('O009', 'C006', 'M002', 1, '2026-09-25 19:30:00', 'completed'),
('O010', 'C007', 'M015', 2, '2026-09-25 21:30:00', 'completed'),
('O011', 'C008', 'M003', 1, '2026-09-26 20:30:00', 'completed'),
('O012', 'C009', 'M029', 1, '2026-09-26 21:30:00', 'completed'),
('O013', 'C010', 'M007', 2, '2026-09-26 18:30:00', 'cancelled'),
('O014', 'C011', 'M013', 1, '2026-09-26 19:45:00', 'completed'),
('O015', 'C012', 'M016', 2, '2026-09-27 20:45:00', 'pending'),
('O016', 'C013', 'M018', 3, '2026-09-27 19:45:00', 'completed'),
('O017', 'C014', 'M021', 2, '2026-09-27 21:30:00', 'completed'),
('O018', 'C015', 'M024', 2, '2026-09-28 18:45:00', 'completed'),
('O019', 'C016', 'M005', 1, '2026-09-28 19:30:00', 'cancelled'),
('O020', 'C017', 'M010', 2, '2026-09-28 20:30:00', 'completed'),
('O021', 'C018', 'M017', 4, '2026-09-28 21:15:00', 'completed'),
('O022', 'C019', 'M020', 1, '2026-09-29 19:45:00', 'pending'),
('O023', 'C020', 'M012', 2, '2026-09-29 20:30:00', 'completed'),
('O024', 'C021', 'M028', 2, '2026-09-29 21:30:00', 'completed'),
('O025', 'C022', 'M019', 4, '2026-09-30 19:30:00', 'completed'),
('O026', 'C023', 'M023', 2, '2026-09-30 18:50:00', 'completed'),
('O027', 'C024', 'M030', 1, '2026-09-30 20:45:00', 'pending'),
('O028', 'C025', 'M008', 2, '2026-10-01 19:45:00', 'completed'),
('O029', 'C026', 'M025', 3, '2026-10-01 20:15:00', 'completed'),
('O030', 'C027', 'M027', 2, '2026-10-01 21:15:00', 'completed');