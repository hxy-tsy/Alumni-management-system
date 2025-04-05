import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count


# 报名参加活动推荐

# 步骤 1：构建用户-活动交互矩阵
def build_user_activity_matrix():
    # 获取所有用户和活动参与记录
    users = User.objects.annotate(
        participated_activities=Count('participated_activities')
    ).filter(participated_activities__gt=0)  # 仅考虑有参与记录的用户

    # 创建用户-活动矩阵（稀疏矩阵）
    matrix = pd.DataFrame(index=[user.id for user in users], columns=['activity_id', 'score'])

    for user in users:
        activities = user.participated_activities.all()
        for activity in activities:
            matrix.loc[user.id, activity.id] = 1  # 1表示参与，可扩展为权重（如报名人数）

    return matrix.fillna(0)  # 填充未参与的活动为0


# 步骤 2：计算活动相似度（基于用户行为）
def calculate_activity_similarity(matrix):
    # 转置矩阵：活动为行，用户为列
    activity_matrix = matrix.T

    # 计算余弦相似度（活动间相似性）
    similarity = cosine_similarity(activity_matrix)

    # 转换为DataFrame方便索引
    activity_ids = list(activity_matrix.index)
    similarity_df = pd.DataFrame(similarity, index=activity_ids, columns=activity_ids)

    return similarity_df


# 步骤 3：结合内容特征增强推荐（可选）
def enhance_with_content_features(activity_id, similarity_df):
    # 获取目标活动的内容特征（如名称、介绍、组织者等）
    target_activity = Activity.objects.get(id=activity_id)
    content_features = f"{target_activity.name} {target_activity.description} {target_activity.organizer}"

    # 对所有活动提取内容特征并计算相似度（示例用TF-IDF）
    from sklearn.feature_extraction.text import TfidfVectorizer

    all_activities = Activity.objects.all()
    content_vectors = TfidfVectorizer().fit_transform(
        [f"{a.name} {a.description} {a.organizer}" for a in all_activities]
    )

    # 计算目标活动与其他活动的内容相似度
    content_similarity = cosine_similarity(
        content_vectors[all_activities.index(target_activity)], content_vectors
    ).flatten()

    # 合并行为相似度和内容相似度（加权平均）
    final_similarity = 0.7 * similarity_df.loc[activity_id] + 0.3 * content_similarity
    return final_similarity.sort_values(ascending=False)


# 步骤 4：生成推荐列表
def recommend_activities(user_id, top_n=5):
    # 获取用户参与过的活动
    user = User.objects.get(id=user_id)
    participated_activities = user.participated_activities.all()

    if not participated_activities:
        return []  # 冷启动处理（推荐热门活动或基于内容推荐）

    # 计算活动相似度（基于用户行为）
    matrix = build_user_activity_matrix()
    similarity_df = calculate_activity_similarity(matrix)

    # 对用户参与过的活动的相似度求和，取top推荐
    recommendations = pd.Series()
    for activity in participated_activities:
        recommendations = recommendations.add(similarity_df.loc[activity.id], fill_value=0)

    # 过滤已参与的活动并排序
    recommendations = recommendations.drop(participated_activities.values_list('id', flat=True))
    recommended_activity_ids = recommendations.sort_values(ascending=False).index[:top_n]

    return Activity.objects.filter(id__in=recommended_activity_ids)
