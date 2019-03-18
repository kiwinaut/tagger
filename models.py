from config import CONFIG
from vdbs.tracker_2_2 import *
from os.path import split

db.init(CONFIG['testdatabase.path'])

create_tagaliases()
import re
pattern = re.compile('\\b[a-zA-Z-]{3,}\\b')

class Query:
    def get_file_path_first(tag_id):
        Archives.select(Archives.filepath)\
        .join(ArchiveTags)\
        .join(Tags)\
        .where(Tags.id==tag_id).limit(1).tuples()

    def get_file_path(file_id):
        row = Archives.get(Archives.id==file_id)
        return row.filepath

    def get_tag_aliases(tag_id):
        q = Aliases.select(Aliases.id, Aliases.alias)\
        .join(Tags)\
        .where(Tags.id==tag_id).tuples()
        return q

    def get_tag_collections(tag_id):
        q = Collections.select(Collections.id, Collections.name)\
        .join(TagCollections)\
        .join(Tags)\
        .where(Tags.id==tag_id).tuples()
        return q


    def add_tag_alias(tag_id, alias):
        alias = alias.strip().lower()
        # print("ALIAS", alias)
        if alias == "":
            raise Exception('Empty String')
        try:
            item = Aliases.get(Aliases.alias==alias)
            # print(item.id, item.alias)
            item.tag_id = tag_id
            item.save()
            iscreated = False
        except Exception as e:
            # print(e)
            item = Aliases.create(alias=alias, tag_id=tag_id)
            iscreated = True
        return item.alias, item.id, iscreated

    def remove_tag_alias(alias_id):
        r = Aliases.delete().where(Aliases.id==alias_id).execute()
        return r

    def add_tag_collection(tid, col):
        col = col.strip().lower()
        if col == "":
            raise Exception('Empty String')
        item, is_col_created = Collections.get_or_create(name=col)
        r, is_j_created = TagCollections.get_or_create(tag_id=tid, collection_id=item.id)
        return item.name, item.id, is_col_created 

    def remove_tag_collection(tag_id, col_id):
        # delete_or_ignore
        return TagCollections.delete().where(TagCollections.tag_id==tag_id, TagCollections.collection_id==col_id).execute()

        # a = TagCollections.get(TagCollections.tag_id==tag_id, TagCollections.collection_id==col_id)
        # r = a.delete_instance()
        # return r


    def tag_findall(text):
        filename = text[:-4].lower()
        res = pattern.findall(filename)
        alias_list = Query.check_alias(res)
        return alias_list


    def get_cols():
        return Collections.select(
                Collections.id, Collections.name
            ).order_by(Collections.name).tuples()


    def get_tree(path='/'):
        return TagTree.select()\
        .where(TagTree.path ** f'{path}%')\
        .order_by(TagTree.path).tuples()

    def set_folder(tag_id, folder_id):
        res= Tags.update(parent=folder_id).where(Tags.id==tag_id).execute()
        return res

    def set_folder_parent(parent_path, child_path):
        # parent_path
        # child_path
        p_path, child_name = split(child_path) # p1/p2, name
        q = f'''
        update tagtree set path = '{parent_path}' ||  substr("path", length('{p_path}')+1)
        where "path" like '{child_path}%';
        '''
        print(q)
        res = db.execute_sql(q)
        new_child_path = f'{parent_path}/{child_name}'
        return res.rowcount, new_child_path

    def new_folder(parent_path, child_name):
        q = f'''
        insert into tagtree ('path','name') values('{parent_path}/{child_name}', '{child_name}')
        '''
        res = db.execute_sql(q)
        return res.rowcount, f'{parent_path}/{child_name}%'

    def delete_folder(path):
        #How many tags it has got
        value = TagTree.select(fn.Count(TagTree.id))\
        .join(Tags)\
        .where(TagTree.path ** f'{path}%')\
        .scalar()
        if value == 0:
            #how many children it has got
            ccount = TagTree.select(fn.Count(TagTree.id))\
            .where(TagTree.path ** f'{path}/%')\
            .scalar()
            if ccount == 0:
                res = TagTree.delete().where(TagTree.path ** f'{path}%').execute()
                return res
            else:
                raise Exception('Folder have folders')

        else:
            raise Exception('Folder have tags')

    def get_tags_by_filter(text):
        sq = Aliases.select(Tags.id, Aliases.alias, Tags.note, Tags.thumb, Tags.flag)\
            .join(Tags)\
            .order_by(Aliases.alias.asc())
        if text == "":
            pass
        else:
            sq=sq.where(Aliases.alias**f"{text}%")
        return sq.tuples()


    def get_tags(col_id=None):
        if col_id is None:
            sq = Aliases.select(Tags.id, Aliases.alias, Tags.note, Tags.thumb, Tags.flag)\
            .join(Tags)\
            .join(TagCollections, JOIN.LEFT_OUTER)\
            .where(TagCollections.collection_id >> None)\
            .order_by(Aliases.alias.asc())
        elif col_id == -1:
            sq = Aliases.select(Tags.id, Aliases.alias, Tags.note, Tags.thumb, Tags.flag)\
            .join(Tags)\
            .order_by(Aliases.alias.asc())
        else:
            # sq = Aliases.select(Tags.id, Aliases.alias)\
            #     .join(Tags)\
            #     .join(TagCollections)\
            #     .join(Collections)\
            #     .where(Collections.id==col_id)\
            #     .order_by(Aliases.alias.asc())
            sq = Aliases.select(Tags.id, Aliases.alias, Tags.note, Tags.thumb, Tags.flag)\
                .join(Tags)\
                .where(Tags.parent_id==col_id)\
                .order_by(Aliases.alias.asc())
        return sq.group_by(Tags.id).tuples()

    def update_tag(tag_id, tag_name, note, rating, thumb, flag):
        r = Tags.update(name=tag_name, note=note, rating=rating, thumb=thumb, flag=flag).where(Tags.id==tag_id).execute()
        if not r:
            raise Exception('Can not update tag')
        return r

    def delete_tag(tag_id):
        r = Tags.delete().where(Tags.id==tag_id).execute()
        if not r:
            raise Exception('Can not delete tag')
        return r

    def check_alias(alias_list):
        # print(alias_list)
        exp = None
        for alias in alias_list:
            s = Aliases.alias ** f"{alias} %"
            if exp:
                exp = exp | s
            else:
                exp = s
            s = Aliases.alias == alias
            exp = exp | s
        sq = Aliases.select(Aliases.id, Aliases.alias).where(exp).tuples()
        # print(sq.sql())
        return sq

    def tables(media):
        if media == 'archives':
            Table = Archives
            j = ArchiveTags
        elif media == 'videos':
            Table = Videos
            j = VideoTags
        elif media == 'collections':
            Table = Collections
            j = ColTags
        return Table, j

    def get_select(media):
        if media == 'archives':
            Table = Archives
            j = ArchiveTags
            select = Table.select(
                Table.id,
                Table.filepath,
                Table.filename,
                Table.size,
                Table.mtime,
                Table.set,
                Table.note,
                Table.count,
                Table.size,#NONE
                # Table.sha,
            )

        elif media == 'videos':
            Table = Videos
            j = VideoTags
            select = Table.select(
                Table.id,
                Table.filepath,
                Table.filename,
                Table.size,
                Table.mtime,
                Table.note,#NONE
                Table.note,
                Table.duration,#NONE
                Table.duration,
                Table.sha,
            )
        return Table, j, select

        
    def add_file_tag(media, fid, tagname=None, tid=None):
        if tagname:
            tag_string = tagname.strip().lower()
            if tag_string == "":
                raise Exception('Empty String')
            try:
                # TAG exist
                alias = Aliases.get(Aliases.alias==tag_string)
                tag = Tags.get(Tags.id == alias.tag_id)
                is_tag_created = False

            except:
                # TAG not exist
                # get file's thumb
                tag = Tags.create(thumb=fid)
                alias = Aliases.create(alias=tag_string, tag_id=tag)
                is_tag_created = True
            RingBuffer.create(alias=alias)
                
            if tag_string.endswith('.com'):
                pass
                #TODO add groups
        elif tid:
            tag = Tags.get(Tags.id==tid)
            alias = Aliases.get(Aliases.tag_id==tag.id)
            is_tag_created = False
        else:
            raise Exception('No tid!')
            
        Table, j = Query.tables(media)
        r = j.insert(tag=tag, file=fid).execute()
        if not r:
            raise Exception('Can not link file and tag')

        alias.lastupdated = datetime.now()
        alias.save()
        return alias.alias.title(), tag.id, is_tag_created
        
    def delete_file_tag(media, fid, tid):
        Table, j = Query.tables(media)
        r = j.delete().where(j.tag==tid, j.file==fid).execute()
        if not r:
            raise Exception('Can not delete file and tag link')
        return r

    def file_tags(file_id):
        Table, j = Query.tables('archives')
        sq = Aliases.select(Tags.id, Aliases.alias)\
        .join(Tags)\
        .join(j)\
        .join(Table)\
        .where(Table.id==file_id)\
        .order_by(Aliases.alias.desc())\
        .group_by(Tags.id).tuples()
        # print(sq.sql())
        return sq

    def get_tag(tag_id):
        return Tags.get(Tags.id==tag_id)

    def get_file(file_id):
        Table, j = Query.tables('archives')
        return Table.get(Table.id==file_id)

    def update_file(media, index, **kw):
        note = kw['note'].strip()
        thumb = kw['thumb'].strip()
        if media == 'archives':
            set = kw['set'].strip()
            Table = Archives
            # j = ArchiveTags
            r = Table.update(set=set, note=note, thumb=thumb, rating=kw['rating']).where(Table.id==index).execute()
        elif media == 'videos':
            Table = Videos
            # j = VideoTags
            r = Table.update(note=note, thumb=thumb).where(Table.id==index).execute()
            if screen == 'true':
                item=Table.get(Table.id==index)
                clip.new_screenshot(item)
        #TODO thumb
        # if kw['rethumb']:
        #     item=Table.get(Table.id==index)
        #     clip.rethumb(item, media, thumb)
        if not r:
            raise Exception('Can not update file')
        return r

    def rethumb(media, ids):
        Table, j = Query.tables(media)
        sq = Table.select(Table.filepath, Table.sha).where(Table.id << ids)
        for q in sq:
            clip.rethumb(q, media)

    def rescreen(media, ids):
        sq = Videos.select(Videos.filepath, Videos.sha).where(Videos.id << ids)
        for q in sq:
            clip.new_screenshot(q)

    def get_tag_groups(tag_id):
        sq = Tags.select(Tags.id, Aliases.alias)\
        .join(Aliases)\
        .switch(Tags)\
        .join(TagCollections)\
        .join(Collections)\
        .where(Collections.name=="group", Tags.id==tag_id)
        return sq



    def get_files(media, sort_string, order_string, *tag_ids, filter=None):
        # Table, j, select = Query.get_select(media)
        # sq = select\
        Table, j = Query.tables(media)
        sq = Table.select(
                Table.id,
                Table.filepath,
                Table.filename,
                Table.size,
                Table.mtime,
                Table.set,
                Table.note,
                Table.count,
                Table.sha
            )\
            .join(j, JOIN.LEFT_OUTER)
            # .join(Tags, JOIN.LEFT_OUTER)\
            # .join(TagTree)\
        if len(tag_ids) == 1:
            sq = sq.where(j.tag_id==tag_ids[0])
        else:
            print(args)
            if args.get('op', '') == 'or':
                sq = sq.where(Tags.tag << tag_list)
            else:pass
        sort = getattr(Table, sort_string)
        order = getattr(sort, order_string)
        if filter:
            sq = sq.where(Table.filename ** filter)
        sq = sq.order_by(order(), Table.mtime.asc())
        return sq.tuples()

    def get_all_files(media, page, sort_string, order_string, filter=None):
        Table, j = Query.tables(media)
        sq = Table.select(
                Table.id,
                Table.filepath,
                Table.filename,
                Table.size,
                Table.mtime,
                Table.set,
                Table.note,
                Table.count,
                Table.sha
            )
        sort = getattr(Table, sort_string)
        order = getattr(sort, order_string)
        print(len(filter), filter)
        if filter:
            sq = sq.where(Table.filename ** filter)
        return sq.order_by(order(), Table.mtime.asc()).paginate(page,50).tuples()

    def get_notag_files(media, page, sort_string, order_string, filter=None):
        Table, j = Query.tables(media)
        sq = Table.select(
                Table.id,
                Table.filepath,
                Table.filename,
                Table.size,
                Table.mtime,
                Table.set,
                Table.note,
                Table.count,
                Table.sha
            )\
        .join(j, JOIN.LEFT_OUTER)\
        .where(j.file_id >> None)

        sort = getattr(Table, sort_string)
        order = getattr(sort, order_string)
        if filter:
            sq = sq.where(Table.filename ** filter)
        return sq.order_by(order(), Table.mtime.asc()).paginate(page,50).tuples()


    def get_tag_column(tag_id, filter=None):
        Table, j = Query.tables('archives')
        sq = Table.select(
                Table.filepath,
            )\
        .join(j, JOIN.LEFT_OUTER)\
        .where(j.tag_id==tag_id)
        if filter:
            sq = sq.where(Table.filename ** filter)

        res = ' '.join([f"\'{q[0]}\'" for q in sq.tuples()])

        return res


    def get_1tag_files(media, page, sort_string, order_string, filter=None):
        Table, j = Query.tables(media)
        sq = Table.select(
                Table.id,
                Table.filepath,
                Table.filename,
                Table.size,
                Table.mtime,
                Table.set,
                Table.note,
                Table.count,
                Table.sha
            )\
            .join(j, JOIN.LEFT_OUTER)\
            .where(j.tag_id.is_null(False))\
            .group_by(Table.id).having(fn.COUNT(Table.id) == 1)

        sort = getattr(Table, sort_string)
        order = getattr(sort, order_string)
        if filter:
            sq = sq.where(Table.filename ** filter)
        return sq.order_by(order(), Table.mtime.asc()).paginate(page,50).tuples()

    def delete_file(media, file_id):
        Table, j = Query.tables(media)
        r = Table.delete().where(Table.id==file_id).execute()
        if r == 0:
            raise Exception(f'Zero Row Affected')
        return r

    def get_tags_by_group(tag_id, media='archive'):
        # q = f'''
        # SELECT "t3"."id", 
        #     "t4"."alias", 
        #     count("t2"."file_id")
        # FROM "archivetags" AS "t2"
        # LEFT OUTER JOIN "tags" AS "t3" ON ("t2"."tag_id" = "t3"."id") 
        # LEFT OUTER JOIN "aliases" AS "t4" ON ("t4"."tag_id" = "t3"."id") 
        # LEFT OUTER JOIN "tagcollections" AS "t5" ON ("t5"."tag_id" = "t3"."id") 
        # LEFT OUTER JOIN "collections" AS "t6" ON ("t5"."collection_id" = "t6"."id")
        # where 
        # "t2"."file_id" IN (
        #     SELECT "t2"."file_id"
        #     FROM "archivetags" AS "t2"
        #     LEFT OUTER JOIN "tags" AS "t3" ON ("t2"."tag_id" = "t3"."id") 
        #     INNER JOIN "aliases" AS "t4" ON ("t4"."tag_id" = "t3"."id") 
        #     LEFT OUTER JOIN "tagcollections" AS "t5" ON ("t5"."tag_id" = "t3"."id") 
        #     LEFT OUTER JOIN "collections" AS "t6" ON ("t5"."collection_id" = "t6"."id")
        #      WHERE ("t4"."alias" == "kelly hall")
        # )
        # GROUP BY "t3"."id"
        # ORDER BY "t4"."alias"        '''
        q= f"""
        SELECT "t3"."id", 
            "t4"."alias", 
            count("t2"."file_id")
        FROM "archivetags" AS "t2"
        LEFT OUTER JOIN "tags" AS "t3" ON ("t2"."tag_id" = "t3"."id") 
        LEFT OUTER JOIN "aliases" AS "t4" ON ("t4"."tag_id" = "t3"."id") 
        LEFT OUTER JOIN "tagcollections" AS "t5" ON ("t5"."tag_id" = "t3"."id") 
        LEFT OUTER JOIN "collections" AS "t6" ON ("t5"."collection_id" = "t6"."id")
        where 
        "t2"."file_id" IN (
            SELECT "t2"."file_id"
            FROM "archivetags" AS "t2"
            LEFT OUTER JOIN "tags" AS "t3" ON ("t2"."tag_id" = "t3"."id") 
            WHERE ("t3"."id" == {tag_id})
        ) AND "t6"."name" == "group"
        GROUP BY "t3"."id"
        ORDER BY "t4"."alias"   
        """
        cursor = db.execute_sql(q)
        return cursor

    def get_tag_details(media, collection=None):
        q = f'''
            SELECT 'a'.'c', COUNT("t2"."id") AS "c", SUM("t2"."size") AS "s"
            FROM "archives" AS "t2" 
            LEFT OUTER JOIN "archivetags" AS "t3" ON ("t3"."file_id" = "t2"."id") 
            LEFT OUTER JOIN "tags" AS "t4" ON ("t3"."tag_id" = "t4"."id")
            LEFT OUTER JOIN(
            SELECT "t4"."id", group_concat("t1"."alias") AS "c"
            from "tags" AS "t4"
            LEFT OUTER JOIN "aliases" AS "t1" ON ("t1"."tag_id" = "t4"."id") 
            GROUP BY  "t4"."id" ORDER BY c DESC
            )as 'a' ON ('a'.'id' = 't4'.'id')
            GROUP BY  "t4"."id" ORDER BY c DESC        '''
        cursor = db.execute_sql(q)
        return cursor
        # Table, j = Query.tables(media)
        # qu = Table.select(
        #         Aliases.alias,
        #         fn.COUNT(Archives.id).alias('c'),
        #         fn.SUM(Archives.size).alias('s')
        #         )\
        #         .join(j, JOIN.LEFT_OUTER)\
        #         .join(Tags, JOIN.LEFT_OUTER)\
        #         .join(Aliases, JOIN.LEFT_OUTER)\
        #         .switch(Tags)\
        #         .join(TagCollections)\
        #         .join(Collections)\
        #         .group_by(Tags.id, Aliases.id)\
        #         .order_by(SQL("c DESC"))
        # print(qu.sql())
        # return qu.tuples()
