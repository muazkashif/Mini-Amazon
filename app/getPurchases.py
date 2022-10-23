#!/usr/bin/env python3
import psycopg2

def getPurchases(user_id):
    conn = psycopg2.connect(
        dbname='/home/vcm/cs316_proj/mini-amazon-skeleton/db/generated/Purchases.csv')
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT *
        FROM Purchases
        WHERE uid = %s''', (user_id))
    except Exception as e:
        print(e)
    for uid, sid, pid, number_of_items, total_amount, time_purchased, order_status in cur:
        print('{} {} {} {} {:,.2f} {} {}'.format(uid, sid, pid, number_of_items, total_amount, time_purchased, order_status))
    
getPurchases(30)
