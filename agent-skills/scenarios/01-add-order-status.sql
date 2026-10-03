ALTER TABLE orders
ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'
CHECK (status IN ('pending', 'paid', 'fulfilled', 'cancelled'));

CREATE INDEX idx_orders_status ON orders(status);
