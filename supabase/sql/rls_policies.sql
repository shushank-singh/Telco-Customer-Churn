ALTER TABLE predictions
ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view their own predictions"

ON predictions

FOR SELECT

USING (
    auth.uid() = user_id
);


CREATE POLICY "Users can insert their own predictions"

ON predictions

FOR INSERT

WITH CHECK (
    auth.uid() = user_id
);