INSERT INTO customers (id, name, tier, active) VALUES
    (1, 'Ada Retail', 'standard', 1),
    (2, 'Byte Works', 'vip', 1),
    (3, 'Curious Labs', 'standard', 1),
    (4, 'Dormant Goods', 'wholesale', 0);

INSERT INTO orders (id, customer_id, ordered_at, total_cents, legacy_note) VALUES
    (101, 1, '2026-09-15', 15000, NULL),
    (102, 2, '2026-09-20', 12000, 'priority account'),
    (103, 2, '2026-09-25', 9000, 'manual adjustment');

INSERT INTO order_items (id, order_id, sku, quantity, unit_price_cents) VALUES
    (1001, 101, 'KEYBOARD', 1, 10000),
    (1002, 101, 'KEYCAPS', 2, 2500),
    (1003, 102, 'MONITOR', 1, 12000),
    (1004, 103, 'DOCK', 1, 8000);
