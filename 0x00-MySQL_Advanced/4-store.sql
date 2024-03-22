-- A SQL script that creates a trigger that decreases
-- the quantity of an item after adding a new order.

DELIMITER //

CREATE TRIGGER decrease_quantity_trigger
    AFTER INSERT ON orders
    FOR EACH ROW
BEGIN
    DECLARE new_quantity INT;

    -- Get the current quantity of the ordered item
    SELECT quantity INTO new_quantity
    FROM items
    WHERE name = NEW.item_name;

    -- Decrease the quantity by the ordered quantity
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END //

DELIMITER ;
