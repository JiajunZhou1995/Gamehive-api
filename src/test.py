from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from nose.tools import assert_true
import requests
import json
import unittest
from app import db,Items,Players,Guilds


class appDBTests(unittest.TestCase):

        
    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        db.create_all()
        self.create_testing_data()
        self.ApiUrl = "http://localhost:5000"

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        db.session.remove()
        db.drop_all()


    def create_testing_data(self):
        data_list = [Players("1","player1","player1@test","1"),
                     Players("2","player2","player2@test"),
                     Players("3","player3","player3@test","NULL"),
                     Items("1","item1",1,"1"),
                     Items("2","item2",2),
                     Items("3","item3",3,"3"),
                     Guilds("1","guild1","1"),
                     Guilds("2","guild2")]

        for data in data_list:
            db.session.add(data)
        db.session.commit()

    def test_root(self):
        url = self.ApiUrl + '/'
        actual = requests.get(url).text
        expect = 'Game Hive Player API'
        self.assertEqual(expect, actual)

    def test_getplayer_success(self):
        url = self.ApiUrl + '/player/1'
        actual = requests.get(url).json()
        expect ={
                    "player_id": "1",
                    "nickname": "player1",
                    "email": "player1@test",
                    "guild_id": "1"
                }
        self.assertEqual(expect, actual)

    def test_getplayer_notsuccess(self):
        url = self.ApiUrl + '/player/100'
        actual = requests.get(url).json()
        expect = {'error':'player doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_createplayer_success(self):
        url = self.ApiUrl + '/player'
        body = {
                "player_id" : "4",
                "nickname" : "name4",
                "email" : "email4",
                "guild_id": "1"
            }
        actual = requests.post(url, json = body).json()
        expect = {'message': 'player added'}
        self.assertEqual(expect, actual)

    def test_createplayer_exists(self):
        url = self.ApiUrl + '/player'
        body = {
                "player_id" : "1",
                "nickname" : "name4",
                "email" : "email4",
                "guild_id": "1"
            }
        actual = requests.post(url, json = body).json()
        expect = {'error':'player exists'}
        self.assertEqual(expect, actual)

    def test_createplayer_notsuccess(self):
        url = self.ApiUrl + '/player'
        body = {
                "player_id" : "4",
                "nickname" : "name4",
                "email" : "email4",
                "guild_id": "4"
            }
        actual = requests.post(url, json = body).json()
        expect = {'error':'guild doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_updateplayer_success(self):
        url = self.ApiUrl + '/player'
        body = {
                "player_id" : "1",
                "nickname" : "name1",
                "email" : "email1",
                "guild_id": "1"
            }
        actual = requests.put(url, json = body).json()
        expect = {'message': 'player updated'}
        self.assertEqual(expect, actual)

    def test_updateplayer_noguild(self):
        url = self.ApiUrl + '/player'
        body = {
                "player_id" : "1",
                "nickname" : "name1",
                "email" : "email1",
                "guild_id": "3"
            }
        actual = requests.put(url, json = body).json()
        expect = {'error':'guild doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_updateplayer_noplayer(self):
        url = self.ApiUrl + '/player'
        body = {
                "player_id" : "4",
                "nickname" : "name1",
                "email" : "email1",
                "guild_id": "1"
            }
        actual = requests.put(url, json = body).json()
        expect = {'error':'player doesn\'t exists'}
        self.assertEqual(expect, actual)

    def test_deleteplayer_success(self):
        url = self.ApiUrl + '/player/1'
        actual = requests.delete(url).json()
        expect = {'message': 'player deleted'}
        self.assertEqual(expect, actual)

    def test_deleteplayer_notsuccess(self):
        url = self.ApiUrl + '/player/4'
        actual = requests.delete(url).json()
        expect = {'error':'player doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_getguild_success(self):
        url = self.ApiUrl + '/guild/1'
        actual = requests.get(url).json()
        expect ={
                    "guild_id": "1",
                    "guild_name": "guild1",
                    "country_code": "1"
                }
        self.assertEqual(expect, actual)

    def test_getguild_notsuccess(self):
        url = self.ApiUrl + '/guild/3'
        actual = requests.get(url).json()
        expect = {'error':'guild doesn\'t exist'}
        self.assertEqual(expect, actual)
        
    def test_createguild_success(self):
        url = self.ApiUrl + '/guild'
        body =  {
                    "guild_id": "3",
                    "guild_name": "guild3",
                    "country_code": "3",
                    "player1_id": "1",
                    "player2_id": "2"
                }
        actual = requests.post(url, json = body).json()
        expect = {'message': 'guild added'}
        self.assertEqual(expect, actual)

    def test_createguild_exists(self):
        url = self.ApiUrl + '/guild'
        body = {
                    "guild_id": "2",
                    "guild_name": "guild3",
                    "country_code": "3",
                    "player1_id": "1",
                    "player2_id": "2"
                }
        actual = requests.post(url, json = body).json()
        expect = {'error':'guild exists'}
        self.assertEqual(expect, actual)

    def test_createguild_notsuccess(self):
        url = self.ApiUrl + '/guild'
        body = {
                    "guild_id": "2",
                    "guild_name": "guild3",
                    "country_code": "3",
                    "player1_id": "4",
                    "player2_id": "5"
                }
        actual = requests.post(url, json = body).json()
        expect = {'error':'player doesn\'t exists'}
        self.assertEqual(expect, actual)

    def test_updateguild_success(self):
        url = self.ApiUrl + '/guild'
        body = {
                "guild_id": "2",
                "guild_name": "guild3",
                "country_code": "3",
            }
        actual = requests.put(url, json = body).json()
        expect = {'message': 'guild updated'}
        self.assertEqual(expect, actual)

    def test_updateguild_noguild(self):
        url = self.ApiUrl + '/guild'
        body = {
                "guild_id" : "3",
                "guild_name": "guild3",
                "country_code": "3",
            }
        actual = requests.put(url, json = body).json()
        expect = {'error':'guild doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_deleteguild_success(self):
        url = self.ApiUrl + '/guild/1'
        actual = requests.delete(url).json()
        expect = {'message': 'guild deleted'}
        self.assertEqual(expect, actual)

    def test_deleteguild_notsuccess(self):
        url = self.ApiUrl + '/guild/3'
        actual = requests.delete(url).json()
        expect = {'error':'guild doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_getitem_success(self):
        url = self.ApiUrl + '/item/1'
        actual = requests.get(url).json()
        expect ={
                    "item_id": "1",
                    "item_name": "item1",
                    "skill_point": 1,
                    "player_id": "1"
                }
        self.assertEqual(expect, actual)

    def test_getitem_notsuccess(self):
        url = self.ApiUrl + '/item/4'
        actual = requests.get(url).json()
        expect = {'error':'item doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_createitem_success(self):
        url = self.ApiUrl + '/item'
        body = {
                    "item_id": "4",
                    "item_name": "item4",
                    "skill_point": 4,
                    "player_id": "1"
                }
        actual = requests.post(url, json = body).json()
        expect = {'message': 'item added'}
        self.assertEqual(expect, actual)

    def test_createitem_exists(self):
        url = self.ApiUrl + '/item'
        body = {
                    "item_id": "1",
                    "item_name": "item4",
                    "skill_point": 4,
                    "player_id": "1"
                }
        actual = requests.post(url, json = body).json()
        expect = {'error':'item exists'}
        self.assertEqual(expect, actual)

    def test_createitem_notsuccess(self):
        url = self.ApiUrl + '/item'
        body = {
                    "item_id": "4",
                    "item_name": "item4",
                    "skill_point": 4,
                    "player_id": "4"
                }
        actual = requests.post(url, json = body).json()
        expect = {'error':'player doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_updateitem_success(self):
        url = self.ApiUrl + '/item'
        body =  {
                    "item_id": "1",
                    "item_name": "item1",
                    "skill_point": 2,
                    "player_id": "1"
                }
        actual = requests.put(url, json = body).json()
        expect = {'message': 'item updated'}
        self.assertEqual(expect, actual)

    def test_updateitem_noplayer(self):
        url = self.ApiUrl + '/item'
        body = {
                    "item_id": "1",
                    "item_name": "item1",
                    "skill_point": 2,
                    "player_id": "4"
                }
        actual = requests.put(url, json = body).json()
        expect = {'error':'player doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_deleteitem_success(self):
        url = self.ApiUrl + '/item/1'
        actual = requests.delete(url).json()
        expect = {'message': 'item deleted'}
        self.assertEqual(expect, actual)

    def test_deleteitem_notsuccess(self):
        url = self.ApiUrl + '/item/4'
        actual = requests.delete(url).json()
        expect = {'error':'item doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_addToGuild_success(self):
        url = self.ApiUrl + '/addToGuild'
        body = {
                    "player_id": "1",
                    "guild_id": "1"
                }
        actual = requests.put(url, json = body).json()
        expect = {'message': "player 1 joined guild 1"}
        self.assertEqual(expect, actual)

    def test_addToGuild_notsuccess(self):
        url = self.ApiUrl + '/addToGuild'
        body = {
                    "player_id": "4",
                    "guild_id": "1"
                }
        actual = requests.put(url, json = body).json()
        expect = {'error':'player or guild doesn\'t exists'}
        self.assertEqual(expect, actual)

    def test_removeFromGuild_success(self):
        url = self.ApiUrl + '/removeFromGuild'
        body = {
                    "player_id": "1",
                    "guild_id": "1"
                }
        actual = requests.put(url, json = body).json()
        expect = {'message': "player 1 left guild 1"}
        self.assertEqual(expect, actual)

    def test_removeFromGuild_notplayer(self):
        url = self.ApiUrl + '/removeFromGuild'
        body = {
                    "player_id": "4",
                    "guild_id": "1"
                }
        actual = requests.put(url, json = body).json()
        expect = {'error':'player doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_removeFromGuild_notguild(self):
        url = self.ApiUrl + '/removeFromGuild'
        body = {
                    "player_id": "1",
                    "guild_id": "4"
                }
        actual = requests.put(url, json = body).json()
        expect = {'error':'guild doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_playerAddItem_success(self):
        url = self.ApiUrl + '/playerAddItem'
        body = {
                    "player_id": "1",
                    "item_id": "1"
                }
        actual = requests.put(url, json = body).json()
        expect = {'message': "item 1 add to player 1"}
        self.assertEqual(expect, actual)

    def test_playerAddItem_noitem(self):
        url = self.ApiUrl + '/playerAddItem'
        body = {
                    "player_id": "1",
                    "item_id": "4"
                }
        actual = requests.put(url, json = body).json()
        expect = {'error':'item doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_playerAddItem_noplayer(self):
        url = self.ApiUrl + '/playerAddItem'
        body = {
                    "player_id": "4",
                    "item_id": "1"
                }
        actual = requests.put(url, json = body).json()
        expect = {'error':'player doesn\'t exist'}
        self.assertEqual(expect, actual)

    def test_calculateGuildPoints_success(self):
        url = self.ApiUrl + '/calculateGuildPoints/1'
        actual = requests.get(url).json()
        expect = {'message': "1"}
        self.assertEqual(expect, actual)

    def test_calculateGuildPoints_notexist(self):
        url = self.ApiUrl + '/calculateGuildPoints/4'
        actual = requests.get(url).json()
        expect = {'error':'guild doesn\'t exist'}
        self.assertEqual(expect, actual)

if __name__ == "__main__":
    unittest.main()