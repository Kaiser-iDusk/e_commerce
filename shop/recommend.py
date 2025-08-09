from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
from .models import Rating

def get_recommendations(user_id, n=5):
    ratings = Rating.objects.all().values('user_id', 'product_id', 'score')
    if not ratings:
        return []
    import pandas as pd
    df = pd.DataFrame(ratings)
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'product_id', 'score']], reader)
    trainset, testset = train_test_split(data, test_size=0.25)
    algo = KNNBasic(sim_options={'user_based': False})
    algo.fit(trainset)
    user_ratings = df[df['user_id'] == user_id]['product_id'].tolist()
    all_products = df['product_id'].unique()
    predictions = [algo.predict(user_id, pid) for pid in all_products if pid not in user_ratings]
    predictions.sort(key=lambda x: x.est, reverse=True)
    top_ids = [pred.iid for pred in predictions[:n]]
    return top_ids