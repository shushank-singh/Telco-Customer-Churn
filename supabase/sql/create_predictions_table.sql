create table predictions (

    id bigint generated always as identity primary key,

    user_id uuid not null,

    customer_data jsonb not null,

    prediction text not null,

    confidence float not null,

    created_at timestamptz default now()

);