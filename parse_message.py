#!/usr/bin/env python

import json
import ipdb
from bs4 import BeautifulSoup

def normalize_user(user, user_map = None):
    if user_map is None or user in user_map:
        return user_map[user]
    return user

def parse_users(text, user_map = None):
    users = []
    for word in text.split(" "):
        word = word.replace(",", "").strip()
        word = normalize_user(word, user_map)
        users.append(word)
    return users

def parse_threads(filename, user_map = None):
    threads = []
    with open(filename) as f:
        soup = BeautifulSoup(f)
        for thread_div in soup.find_all("div", { "class": "thread" }):
            users = parse_users(thread_div.find(text=True), user_map)
            messages = []
            for message_div in thread_div.find_all("div", { "class": "message" }):
                user = message_div.find("span", { "class": "user" }).text
                user = normalize_user(user, user_map)
                date = message_div.find("span", { "class": "meta" }).text
                text = message_div.find_next_sibling("p").text
                messages.append({ "user": user, "date": date, "text": text })
            threads.append({ "users": users, "messages": messages })
    return threads

def read_user_map(filename):
    with open(filename) as f:
        return json.load(f)

def main():
    user_map = read_user_map("users.json")
    threads = parse_threads("html/messages.htm", user_map)
    with open("threads.json", "w") as f:
        json.dump(threads, f, indent = 2)


if __name__ == "__main__":
    main()

