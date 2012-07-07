#!/usr/bin/env python
# -*- coding:utf-8 -*-
from nose.tools import *
import sys
sys.path.append('../lib')
import qbp

class TestRedisConnection():
    """
    RedisConnection/RedisOperatorの動作用テスト
    Redisに関する動作を司るクラス
    """
    
    def setup(self):
        # 新しいredisconnectionを追加
        self.key_prefix = '__qbp_unittest_01_2011'
        self.redis_connection = qbp.RedisConnection('localhost', 6379, self.key_prefix)

    def teardown(self):
        # 使ってたキーを削除
        key_list = self.redis_connection.keys('*')
        for key in key_list:
            self.redis_connection.delete(key)

    # infoコマンドのテスト
    def test_info_command(self):
        result = self.redis_connection.info()
        eq_(len(result) > 0, True)

    # lpush/rpopコマンド
    def test_push_pop_command(self):
        result = self.redis_connection.lpush('hogehoge', 'foo')
        eq_(result, 1L)
        result = self.redis_connection.rpop('hogehoge')
        eq_(result, 'foo')

    # key_prefixを設定したものを足しているときはkey_prefixを追加しないでアクセスできる
    def test_key_prefix(self):
        result = self.redis_connection.lpush('hogehoge', 'bar')
        eq_(result, 1L)
        result = self.redis_connection.rpop('%s:hogehoge' % self.key_prefix)
        eq_(result,'bar')
        
    # 存在しないコマンド
    def test_invalid_command(self):
        assert_raises(AttributeError, self.redis_connection.hoge, 'hoge')
        
        
        
        
