from secrets import settings
import tweepy, os
import unicodecsv as csv

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
    return [api.get_user(follower).screen_name for follower in api.followers_ids(user_id)]

r = retrieve_followers("AllenDowney")
timeit.timeit(r)

def retrieve_friends(user_id):
    return [api.get_user(friend).screen_name for friend in api.friends_ids(user_id)]

r = retrieve_friends("AllenDowney")
timeit.timeit(r)

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
                retrieve_network(n + 1, friend)

def write_dict_to_csv(network):
    with open('results.csv', 'wb') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter='\t')
        for user in network:
            for attribute in network[user]:
                    csvwriter.writerow([user, attribute, str(network[user][attribute])])
        csv_file.close()

def read_csv(csv_file):
    # to be filled in
    pass

def main():
    retrieve_network(0, 'AllenDowney')
    print(network)

# main()

print("Completed!")