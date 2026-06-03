from supabase_utils.client import supabase


def save_prediction(
    user_id,
    customer_data,
    prediction,
    confidence
):

    data = {

        "user_id": user_id,

        "customer_data": customer_data,

        "prediction": prediction,

        "confidence": confidence
    }

    response = (
        supabase
        .table("predictions")
        .insert(data)
        .execute()
    )

    return response



def get_user_predictions(user_id):

    response = (

        supabase
        .table("predictions")
        .select("*")
        .eq("user_id", user_id)
        .order(
            "created_at",
            desc=True
        )
        .execute()

    )

    return response.data