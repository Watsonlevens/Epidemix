import tweepy, os, csv

consumer_key = os.environ.get("API_KEY", '')
consumer_secret = os.environ.get("API_SECRET", '')
access_token = os.environ.get("ACCESS_KEY", '')
access_token_secret = os.environ.get("ACCESS_SECRET", '')

print("Initializing...")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit = True)

network = {}

def retrieve_followers(user_id):
    followers = []
    for follower in api.followers_ids(user_id):
        followers.append(api.get_user(follower).screen_name)
    return followers

def retrieve_friends(user_id):
    users = []
    page_count = 0
    for user in tweepy.Cursor(api.friends, id=user_id, count=200).pages():
        page_count += 1
        users.extend(user)
    return users

def retrieve_network(n, user_id):
    if n == 6:
        return
    else:
        followers = retrieve_followers(user_id)
        friends = retrieve_friends(user_id)
        if user_id not in network:
            network[user_id]['followers'] = followers
            network[user_id]['friends'] = friends
            for follower in followers:
                retrieve_network(n + 1, follower)
            for friend in friends:
                retrieve_network(n + 1, follower)

def write_dict_to_csv(network):
    with open('results.csv', 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter='\t')
        for user in network:
            for attribute in network[user]:
                csvwriter.writerow([user, attribute, network[user][attribute]])

def main():
    retrieve_network(0, api.followers_ids('AllenDowney'))
    print(network)

main()

print("Completed!")