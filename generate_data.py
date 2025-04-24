import pandas as pd
import numpy as np

n_clusters = 4
np.random.seed(42)

regions = ["EMEA", "APAC", "AMERICAS"]
region_probs = [0.4, 0.3, 0.3]  # Adjust as needed

feature_names = [
    "TOTAL_SPEND_WATCHES", "TOTAL_SPEND_ACCESSORIES", "TOTAL_SPEND_BAGS", "TOTAL_SPEND_WALLETS", "TOTAL_SPEND_JEWELRY",
    "EMAIL_CLICK_RATE", "DAYS_SINCE_LAST_EMAIL_CLICK", "MOBILE_SESSION_SHARE", "DESKTOP_SESSION_SHARE",
    "IS_MALE", "IS_FEMALE", "IS_18_24", "IS_25_34", "IS_35_44", "IS_45_54", "IS_55_PLUS",
    "SPENT_ON_BLACK_FRIDAY", "SPENT_IN_HOLIDAY_SEASON", "SPENT_AROUND_VALENTINE"
]

def generate_mock_data(samples_per_cluster=100):
    mock_data = []
    for i in range(n_clusters):
        for _ in range(samples_per_cluster):
            cluster = {"CLUSTER": f"Cluster {i+1}"}
            cluster["REGION"] = np.random.choice(regions, p=region_probs)
            age_group = np.random.choice(["IS_18_24", "IS_25_34", "IS_35_44", "IS_45_54", "IS_55_PLUS"], p=[0.2, 0.25, 0.25, 0.15, 0.15])
            male = np.random.randint(0, 2)
            cluster["IS_MALE"] = male
            cluster["IS_FEMALE"] = 1 - male

            for feature in feature_names:
                if feature in ["IS_MALE", "IS_FEMALE"]:
                    continue
                elif feature.startswith("IS_"):
                    cluster[feature] = int(feature == age_group)
                elif feature in ["MOBILE_SESSION_SHARE", "DESKTOP_SESSION_SHARE"]:
                    mobile_share = np.clip(np.random.normal(0.8, 0.1), 0.6, 1.0) if age_group in ["IS_18_24", "IS_25_34", "IS_35_44"] else np.clip(np.random.normal(0.3, 0.1), 0.0, 0.6)
                    cluster["MOBILE_SESSION_SHARE"] = mobile_share
                    cluster["DESKTOP_SESSION_SHARE"] = 1 - mobile_share
                elif feature == "SPENT_ON_BLACK_FRIDAY":
                    cluster[feature] = np.random.uniform(200, 400) if age_group == "IS_18_24" else np.random.uniform(10, 100)
                elif feature == "SPENT_AROUND_VALENTINE":
                    cluster[feature] = np.random.uniform(150, 350) if age_group == "IS_25_34" else np.random.uniform(10, 100)
                elif feature == "SPENT_IN_HOLIDAY_SEASON":
                    cluster[feature] = np.random.uniform(50, 250)
                elif feature == "EMAIL_CLICK_RATE":
                    cluster[feature] = np.round(np.random.uniform(0.05, 0.4), 2)
                elif feature == "DAYS_SINCE_LAST_EMAIL_CLICK":
                    cluster[feature] = np.random.randint(1, 90)
                elif feature == "TOTAL_SPEND_WATCHES":
                    cluster[feature] = np.random.uniform(300, 500) if male else np.random.uniform(10, 100)
                elif feature == "TOTAL_SPEND_WALLETS":
                    cluster[feature] = np.random.uniform(100, 250) if male else np.random.uniform(10, 50)
                elif feature == "TOTAL_SPEND_JEWELRY":
                    cluster[feature] = np.random.uniform(300, 500) if not male else np.random.uniform(10, 50)
                elif feature == "TOTAL_SPEND_BAGS":
                    cluster[feature] = np.random.uniform(200, 400) if not male else np.random.uniform(10, 50)
                elif feature == "TOTAL_SPEND_ACCESSORIES":
                    cluster[feature] = np.random.uniform(20, 150)

            mock_data.append(cluster)
    return pd.DataFrame(mock_data)

# Generate and save
data = generate_mock_data(samples_per_cluster=100)
data["TOTAL_SPEND"] = data[[
    "TOTAL_SPEND_WATCHES", "TOTAL_SPEND_ACCESSORIES", "TOTAL_SPEND_BAGS", "TOTAL_SPEND_WALLETS", "TOTAL_SPEND_JEWELRY"
]].sum(axis=1)
data.to_csv("mock_data.csv", index=False)
