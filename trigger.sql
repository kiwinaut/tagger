#attach
attach database 'db/contacts.db' as '21';



#tagtree
insert into tagtree  ('id', 'path', 'name')  
select id, path, name  from '21'.'tagtree'
#tags
insert into tags (id, note, flag, name, rating, parent_id, thumb)  
select id, note, flag, name, rating, parent_id, thumb  from '21'.'tags'
#aliases
insert into aliases  ('alias', 'tag_id')  
select alias, tag_id  from '21'.'aliases'
#
insert into archives  
select *  from '21'.'archives'
#
insert into archivetags 
select *  from '21'.'archivetags'


CREATE TRIGGER alias_update_trigger
	AFTER UPDATE
	ON ALIASES
	WHEN OLD.tag_id != NEW.tag_id
	BEGIN	
		UPDATE OR REPLACE "archivetags"
		SET "tag_id" = NEW."tag_id"
		WHERE "archivetags"."tag_id" in (
			SELECT "tags"."id" FROM "tags" 
			LEFT JOIN "aliases" ON "aliases"."tag_id" == "tags"."id"
			where "aliases"."id" is NULL AND "tags"."id"= OLD."tag_id"
		);

		UPDATE OR REPLACE "videotags"
		SET "tag_id" = NEW."tag_id"
		WHERE "videotags"."tag_id" in (
			SELECT "tags"."id" FROM "tags" 
			LEFT JOIN "aliases" ON "aliases"."tag_id" == "tags"."id"
			where "aliases"."id" is NULL AND "tags"."id"= OLD."tag_id"
		);

		UPDATE OR REPLACE "tagcollections"
		SET "tag_id" = NEW."tag_id"
		WHERE "tagcollections"."tag_id" in (
			SELECT "tags"."id" FROM "tags" 
			LEFT JOIN "aliases" ON "aliases"."tag_id" == "tags"."id"
			where "aliases"."id" is NULL AND "tags"."id"= OLD."tag_id"
		);

		-- Deletes tag that have zero aliases
		DELETE FROM "tags"
		WHERE "tags"."id" in (
			SELECT "tags"."id" FROM "tags" 
			LEFT JOIN "aliases" ON "aliases"."tag_id" == "tags"."id"
			where "aliases"."id" is NULL AND "tags"."id"= OLD."tag_id"
		);
	END;


CREATE TRIGGER alias_del_trigger
	AFTER DELETE
	ON "aliases"
	BEGIN
		-- Deletes tag that have zero aliases
		DELETE FROM "tags"
		WHERE "tags"."id" in (
			-- select tags with null alias
			SELECT "tags"."id" FROM "tags" 
			LEFT JOIN "aliases" ON "aliases"."tag_id" == "tags"."id"
			where "aliases"."id" is NULL AND "tags"."id"= OLD."tag_id"
		);
	END;

CREATE TRIGGER tag_del_trigger
	AFTER DELETE
	ON "tags"
	BEGIN
		-- delete archive_tags
		DELETE FROM "archivetags" WHERE "tag_id" == OLD."id";
		-- delete video_tags
		DELETE FROM "videotags" WHERE "tag_id" == OLD."id";
		-- delete tag_collections
		DELETE FROM "tagcollections" WHERE "tag_id" == OLD."id";
		-- delete aliases
		DELETE FROM "aliases" WHERE "tag_id" == OLD."id";
	END;

CREATE TRIGGER archive_del_trigger
	AFTER DELETE
	ON "archives"
	BEGIN
		DELETE FROM "archivetags" WHERE "file_id" == OLD."id";
	END;

CREATE TRIGGER video_del_trigger
	AFTER DELETE
	ON "videos"
	BEGIN
		DELETE FROM "videotags" WHERE "file_id" == OLD."id";
	END;

CREATE TRIGGER col_del_trigger
	AFTER DELETE
	ON "collections"
	BEGIN
		DELETE FROM "tagcollections" WHERE "collection_id" == OLD."id";
	END;

CREATE TRIGGER tagcol_del_trigger
	AFTER DELETE
	ON "tagcollections"
	BEGIN
		DELETE FROM "collections"
		WHERE "collections"."id" in (
			SELECT "collections"."id" FROM "collections" 
			LEFT JOIN "tagcollections" ON "tagcollections"."collection_id" == "collections"."id"
			where "tagcollections"."collection_id" is NULL AND "collections"."id"= OLD."collection_id"
		);
	END;

-- ringbuffer
CREATE TRIGGER delete_tail AFTER INSERT ON "RingBuffer"
BEGIN
    DELETE FROM "RingBuffer" WHERE id%20=NEW.id%20 AND id!=NEW.id;
END;


-- deletes Js have no tags
delete from archivetags
where archivetags.tag_id in
(
select archivetags.tag_id from archivetags
LEFT OUTER JOIN tags on archivetags.tag_id == tags.id
where tags.id is null
)

-- duplicates
delete from 'videos'
where id in (
select id from 'videos' 
group by 'videos'.'sha' having (COUNT(*) >1)
)


-- update from query
update tags set name=
 (
select Aliases.alias  from Aliases 
where Aliases.tag_id == tags.id
group by Aliases.tag_id
)
where Tags.name == "" or Tags.name is null

-- find duplicates
select *, count(alias) from aliases
group by alias having (count(alias) > 1)

-- tags have no alias
select * from tags
left join aliases on aliases.tag_id == tags.id
where aliases.tag_id is Null