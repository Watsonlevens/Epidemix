from secrets import settings
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
    friends = []
    page_count = 0
    for friend in api.friends_ids(user_id):
        friends.append(api.get_user(friend).screen_name)
    return friends

def retrieve_network(n, user_id):
    if n == 6:
        return
    else:
        followers = retrieve_followers(user_id)
        friends = retrieve_friends(user_id)

        if user_id not in network:
            network[user_id]['followers'] = follower
            network[user_id]['friends'] = friends
            for follower in followers:
                retrieve_network(n + 1, follower)
            for friend in friends:
                retrieve_network(n + 1, follower)

    print("This is iteration " + n)

def write_dict_to_csv(network):
    with open('results.csv', 'w') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter='\t')
        for user in network:
            for attribute in network[user]:
                csvwriter.writerow([user, attribute, network[user][attribute]])

def main():
    retrieve_network(0, 'AllenDowney')
    print(network)

main()

print("Completed!")