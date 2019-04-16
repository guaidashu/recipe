# author songjie
create table `recipe_list`(
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'recipe primary key',
    `name` varchar(255) NOT NULL COMMENT 'recipe`s name',
    `url` varchar(255) NOT NULL COMMENT ' recipe content url',
    `img_url` varchar(255) NOT NULL COMMENT 'recipe img url',
    `introduce` text NOT NULL COMMENT 'recipe introduce',
    `page_views` int(11) NOT NULL COMMENT 'recipe visit num',
    `recipe_type_id` int(11) NOT NULL COMMENT 'recipe`s type id',
    `status` int(1) NOT NULL COMMENT 'it`s used to mark that whether the recipe is get.',
    PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

create table `recipe_type`(
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'recipe`s type id',
    `name` varchar(255) NOT NULL COMMENT 'recipe type name',
    `page_num` longtext NOT NULL COMMENT 'page num(a json data)',
    `keyword` varchar(255) NOT NULL COMMENT 'website`s origin search keyword',
    `nav_type` int(1) NOT NULL COMMENT 'nav type 1 is root node, 0 is child node, if it`s 2, you can search its child according id union parent_id',
    `parent_id` int(11) NOT NULL COMMENT 'type`s parent id(because type maybe has children)',
    PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

create table `recipe_content`(
    `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'recipe content table` id',
    `name` varchar(255) NOT NULL COMMENT 'recipe name',
    `img_url` varchar(255) NOT NULL COMMENT 'recipe img url',
    `video_id` varchar(255) NOT NULL COMMENT 'recipe video id(Youtube)',
    `preparation` longtext NOT NULL COMMENT 'recipe preparation, it`s a json data',
    `ingredients` text NOT NULL COMMENT 'the ingredients which recipe needs',
    `list_id` int(11) NOT NULL COMMENT 'the list id which is used to pattern',
    PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
