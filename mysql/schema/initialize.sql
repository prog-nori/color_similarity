CREATE DATABASE minecraft_utility;
use minecraft_utility;

-- アップロードされた画像の格納パスとidを紐付ける。
-- idは10桁のランダムな数字（[a-zA-z]を混ぜても良いかも）
create table if not exists images (
    id varchar(11),
    filename varchar(255)
);

-- ブロック関連の情報を格納する
create table if not exists blocks (
    -- 最も長いブロックidはsculk_shrieker_can_summon_inner_topの35なので綺麗なところで64とする
    texture_id varchar(64),
    -- red平均値
    red int,
    -- green平均値
    green int,
    -- blue平均値
    blue int,
    -- rgb平均値
    rgb varchar(20),
    -- 論理除外フラグ
    ignore_flag boolean
);

-- どのブロックのテクスチャなのかを明らかにする
create table if not exists textures (
    -- ブロックid
    texture_group_id varchar(64),
    -- ブロック名
    name varchar(64),
    -- テクスチャid
    texture_id varchar(64)
);

-- -- 検索ログ（ブロック名）
-- create table if not exists search_log (
-- )


-- -- マイクラWiki閲覧ログ
-- create table if not EXISTS view_minecraft_wiki_log (
-- )

-- -- 画像検索ログ
-- create table if not exists image_search_log (
--     filename varchar(255),
--     first_search_at datetime,
--     last_search_at datetime,
--     search_count int
-- )

