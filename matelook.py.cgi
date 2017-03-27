#!/usr/bin/env python3.5

#Written by Zhimai Wang, stuId: z5051569
#For COMP9041, Assignment 2


import cgi, cgitb, glob, os, sqlite3, re
from http import cookies
from time import sleep
from datetime import datetime
import smtplib

def main():
    # print(page_header()) #head
    cgitb.enable()
    users_dir = "dataset-medium"
    parameters = cgi.FieldStorage() #get data from field/form
    # print(user_page(parameters, users_dir))
    if parameters.getvalue('url') == 'verify_user':
        print(verify_user(parameters))
    elif parameters.getvalue('url') == 'user_homepage':
        print(user_homepage(parameters))
        print(mate_list(parameters))
        print(navigation(parameters))
        print(search_bar(parameters))
        print(make_post_field(parameters))
        print(recent_post(parameters))
    elif parameters.getvalue('url') == 'mate_homepage':
        current_user = parameters.getvalue('current_user')
        zid = parameters.getvalue('zid')
        print(user_homepage(parameters))
        print(mate_list(parameters))
        print(navigation(parameters))
        print(search_bar(parameters))
        if current_user == zid:
            print(make_post_field(parameters))
        print(recent_post(parameters))
    elif parameters.getvalue('url') == 'search_name':
        print(search_name(parameters))
    elif parameters.getvalue('url') == 'search_post':
        print(search_post(parameters))
    elif parameters.getvalue('url') == 'make_post':
        print(make_post(parameters))
    elif parameters.getvalue('url') == 'new_comment':
        print(new_comment(parameters))
    elif parameters.getvalue('url') == 'new_reply_field':
        print(new_reply_field(parameters))
    elif parameters.getvalue('url') == 'new_reply':
        print(new_reply(parameters))
    elif parameters.getvalue('url') == 'post_detail':
        print(post_detail(parameters))
    elif parameters.getvalue('url') == 'create_account_field':
        print(create_account_field(parameters))
    elif parameters.getvalue('url') == 'create_account':
        print(create_account(parameters))
    elif parameters.getvalue('url') == 'update_info_field':
        print(update_info_field(parameters))
    elif parameters.getvalue('url') == 'update_info':
        print(update_info(parameters))
    elif parameters.getvalue('url') == 'delete_post_confirm':
        print(delete_post_confirm(parameters))
    elif parameters.getvalue('url') == 'delete_post':
        print(delete_post(parameters))
    elif parameters.getvalue('url') == 'delete_comment_confirm':
        print(delete_comment_confirm(parameters))
    elif parameters.getvalue('url') == 'delete_comment':
        print(delete_comment(parameters))
    elif parameters.getvalue('url') == 'delete_reply_confirm':
        print(delete_reply_confirm(parameters))
    elif parameters.getvalue('url') == 'delete_reply':
        print(delete_reply(parameters))
    else:
        print(index(parameters))
    print(page_trailer(parameters)) #tail




def index(parameters):
    print(page_header())
    with open(os.path.join('templates', 'index.html')) as file:
        return file.read()

def verify_user(parameters):
    zid = parameters.getvalue('zid')
    password = parameters.getvalue('password')
    print(page_header())
    sql = "SELECT * FROM USER_INFO WHERE ZID=\'{}\' AND PASSWORD=\'{}\'"
    arguments = [zid, password]
    cursor = query(sql, arguments)
    if cursor.fetchone():
        return """
    <form name="user_homepage" method="POST" action="?url=user_homepage">
    <input type="hidden" name="zid" value="{zid}">
    <input type="hidden" name="current_user" value="{zid}">
    </form>
    <script TYPE="text/JavaScript">
        document.forms["user_homepage"].submit()
        
    </script>
    """.format(zid=zid)
    else:
        return """
        <div align="center">
        <form method="POST" action="?url=index">
            <p>Your password is wrong, please try again.</p>
            <input type="submit" value="BACK">
        </form>
        </div
    """

def user_homepage(parameters):
    zid = parameters.getvalue('zid')
    current_user = parameters.getvalue('current_user')
    print(page_header())

    if os.path.exists(os.path.join('dataset-medium',zid, 'profile.jpg')):
        profile = os.path.join('dataset-medium',zid, 'profile.jpg')
    else:
        profile = os.path.join('images','no_profile.png')

    sql = "SELECT * FROM USER_INFO WHERE ZID=\'{}\'"
    arguments = [zid]
    cursor = query(sql, arguments)

    for row in cursor:
        username = row[1]
        birthday = row[3]
        home_suburb = row[4]
        program = row[7]
        mates = row[9]
        detail = row[11]

    if not detail:
        detail = 'Nothing'
    return """
<div class="matelook_left_bar">
    <div>
        <div class="matelook_display_container">
            <img src=\"%s\" alt="No Profile">
        </div>
        <div class="matelook_container">
            <p>Name: %s</p>
            <p>Birthday: %s</p>
            <p>Home Suburb: %s</p>
            <p>Program: %s</p>
            <p>Self Introduction: %s</p>
            
""" % (profile, username, birthday, home_suburb, program, detail)

def mate_list(parameters):
    zid = parameters.getvalue('zid')
    current_user = parameters.getvalue('current_user')
    #mate name
    sql = "SELECT MATES FROM USER_INFO WHERE ZID=\'{}\'"
    arguments = [zid]
    cursor = query(sql, arguments)
    commom_header = """
                <p>Mate List:</p><br>
    """
    commom_tail = """
                <br>
            </div>
        </div><br>
    </div>
    <p>
    """

    for row in cursor:
        mates = row[0]

    if mates:
        mates = mates.split(',')
        with open(os.path.join('templates','matelist_user_homepage.html')) as file:
            mate_template = file.read()
        mate_part = ''
        for mate_id in mates:
            mate_id = mate_id.strip()
            sql = "SELECT USERNAME FROM USER_INFO WHERE ZID=\'{}\'"
            arguments = [mate_id]
            cursor = query(sql, arguments)
            for row in cursor:
                mate_name = row[0]
            if os.path.exists(os.path.join('dataset-medium',mate_id, 'profile.jpg')):
                mate_profile = os.path.join('dataset-medium', mate_id, 'profile.jpg')
            else:
                mate_profile = os.path.join('images','no_profile.png')
            mate_part += mate_template.format(mate_name=mate_name, mate_id=mate_id, profile=mate_profile, current_user=current_user)

        
        return commom_header + mate_part + commom_tail
    else:
        return commom_header + commom_tail


def navigation(parameters):
    current_user = parameters.getvalue('current_user')

    return """
    <div class="matelook_navigation">
    <table>
    <tr>
    <td>
    <form method="POST" action="?url=user_homepage">
    <a href="javascript:;" onclick="parentNode.submit();">Homepage</a>
    <input type="hidden" name="zid" value="{current_user}">
    <input type="hidden" name="current_user" value="{current_user}">
    </form>
    </td>

    <td>
    <form method="POST" action="?url=update_info_field">
    <a href="javascript:;" onclick="parentNode.submit();">Update Info</a>
    <input type="hidden" name="zid" value="{current_user}">
    <input type="hidden" name="current_user" value="{current_user}">
    </form>
    </td>

    <td>
    <form method="POST" action="?url=">
    <a href="javascript:;" onclick="parentNode.submit();">Logout</a>
    </form>
    </td>
    </tr>
    </table>
    </div>
    <br>
""".format(current_user=current_user)


def search_bar(parameters):
    current_user = parameters.getvalue('current_user')
    with open(os.path.join('templates', 'search_bar.html')) as file:
        return file.read().format(current_user=current_user)



def search_post(parameters):
    print(page_header())
    print(navigation(parameters))
    current_user = parameters.getvalue('current_user')
    post = parameters.getvalue('post').lower()
    if "'" not in post:
        sql = "SELECT * FROM POST WHERE LOWER(MESSAGE) LIKE \'%{}%\'"
        arguments = [post]
        with open(os.path.join('templates', 'post_search.html')) as file:
            post_template = file.read()
        post_part = ''
        cursor = query(sql, arguments)
        post_search_result = cursor.fetchall()
        if len(post_search_result) > 0:
            for row in post_search_result:
                post_id = row[0]
                zid = row[1]
                message = row[2].encode('ascii', 'ignore').decode('ascii')
                time = row[3]
                zid_name = get_name(zid)
                comment_number = get_comment_count(post_id)
                post_part += post_template.format(zid=zid, zid_name=zid_name, message=message, time=time, current_user=current_user, comment_number=comment_number, post_id=post_id)

            commom_header = """
                        <p align="center">Your result:</p><br>
        """
            return commom_header + post_part
        else:
            message = "There is no result."
            with open(os.path.join('templates', 'empty_result.html')) as file:
                return file.read().format(message=message, current_user=current_user)
    else:
        with open(os.path.join('templates', 'search_error.html')) as file:
            return file.read().format(current_user=current_user)


def search_name(parameters):
    print(page_header())
    print(navigation(parameters))
    current_user = parameters.getvalue('current_user')
    username = parameters.getvalue('username').lower()
    if "'" not in username:
        sql = "SELECT * FROM USER_INFO WHERE LOWER(USERNAME) LIKE \'%{}%\'"
        arguments = [username]
        cursor = query(sql, arguments)
        mate_search_result = cursor.fetchall()
        with open(os.path.join('templates', 'matelist_search.html')) as file:
            mate_template = file.read()
        mate_part = ''
        if len(mate_search_result) > 0:
            for row in mate_search_result:
                mate_id = row[0]
                mate_name = row[1]
                if os.path.exists(os.path.join('dataset-medium',mate_id, 'profile.jpg')):
                    mate_profile = os.path.join('dataset-medium', mate_id, 'profile.jpg')
                else:
                    mate_profile = os.path.join('images','no_profile.png')
                mate_part += mate_template.format(mate_name=mate_name, profile=mate_profile, mate_id=mate_id, current_user=current_user)

            commom_header = """
                    <p align="center">You may find:</p><br>
        """
            
            return commom_header + mate_part
        else:
            message = "Your mates maybe not register in MATELOOK. You could recommend MATELOOK for them. : )"
            with open(os.path.join('templates', 'empty_result.html')) as file:
                return file.read().format(message=message, current_user=current_user)
    else:
        with open(os.path.join('templates', 'search_error.html')) as file:
            return file.read().format(current_user=current_user)


def make_post_field(parameters):
    zid = parameters.getvalue('zid')
    current_user = parameters.getvalue('current_user')
    with open(os.path.join('templates', 'make_post_field.html')) as file:
        return file.read().format(zid=zid, current_user=current_user)

def make_post(parameters):
    print(page_header())
    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('zid')
    post = parameters.getvalue('post')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO POST (ZID, MESSAGE, TIME) VALUES (?, ?, ?)"
    conn = sqlite3.connect('user.db')
    conn.execute(sql, (current_user, post, time))
    conn.commit()
    return """
    <form name="user_homepage" method="POST" action="?url=user_homepage">
    <input type="hidden" name="zid" value="{current_user}">
    <input type="hidden" name="current_user" value="{current_user}">
    </form>
    <script TYPE="text/JavaScript">
        document.forms["user_homepage"].submit()
    </script>
""".format(current_user=current_user)



def recent_post(parameters):
    zid = parameters.getvalue('zid')
    current_user = parameters.getvalue('current_user')

    sql = "SELECT POST_ID, MESSAGE, TIME FROM POST WHERE ZID = \'{}\' ORDER BY TIME DESC"
    arguments = [zid]
    cursor = query(sql, arguments)

    if current_user == zid:
        with open(os.path.join('templates', 'recent_post_current_user.html')) as file:
            post_part_template = file.read()
    else:
        with open(os.path.join('templates', 'recent_post_others.html')) as file:
            post_part_template = file.read()
    post_part = ''
    for row in cursor:
        post_id = row[0]
        time = row[2].replace('T', ' ')
        time = re.sub(r'\+\d*', '', time)
        message = row[1].encode('ascii', 'ignore').decode('ascii')
        comment_number = get_comment_count(post_id)
        post_part += post_part_template.format(zid=zid, post_id=post_id, time=time, message=message, comment_number=comment_number, current_user=current_user)

    commom_header = """
<div class="matelook_right_bar">
    <div class="matelook_display_container">
        <h2 class="matelook_title">Recent Post</h2>
        <div class="matelook_display_container">
"""
    commom_tail = """
        </div>
    </div>
</div>
"""
    return commom_header + post_part + commom_tail


def new_comment(parameters):
    print(page_header())
    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('zid')
    post_id = parameters.getvalue('post_id')
    time = parameters.getvalue('time')
    message = parameters.getvalue('message')
    new_comment = parameters.getvalue('new_comment')
    time_comment = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = "INSERT INTO COMMENT (FROM_ZID, TO_POST_ID, MESSAGE, TIME) VALUES (?, ?, ?, ?)"
    conn = sqlite3.connect('user.db')
    conn.execute(sql, (current_user, post_id, new_comment, time_comment))
    conn.commit()

    return """
    <form name="post_detail" method="POST" action="?url=post_detail">
    <input type="hidden" name="post_id" value="{post_id}">
    <input type="hidden" name="time" value="{time}">
    <input type="hidden" name="message" value="{message}">
    <input type="hidden" name="current_user" value="{current_user}">
    <input type="hidden" name="zid" value="{zid}">
    </form>
    <script TYPE="text/JavaScript">
        document.forms["post_detail"].submit()
        
    </script>
""".format(post_id=post_id, time=time, message=message, current_user=current_user, zid=zid)



def new_reply(parameters):
    print(page_header())
    post_id = parameters.getvalue('post_id')
    time = parameters.getvalue('time')
    message = parameters.getvalue('message')
    comment_id = parameters.getvalue('comment_id')
    time_reply = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_reply = parameters.getvalue('new_reply')

    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('zid')
    sql = "INSERT INTO REPLY (FROM_ZID, TO_COMMENT_ID, MESSAGE, TIME) VALUES (?, ?, ?, ?)"
    conn = sqlite3.connect('user.db')
    conn.execute(sql, (current_user, comment_id, new_reply, time_reply))
    conn.commit()
    return """
    <form name="post_detail" method="POST" action="?url=post_detail">
    <input type="hidden" name="post_id" value="{post_id}">
    <input type="hidden" name="time" value="{time}">
    <input type="hidden" name="message" value="{message}">
    <input type="hidden" name="current_user" value="{current_user}">
    <input type="hidden" name="zid" value="{zid}">
    </form>
    <script TYPE="text/JavaScript">
        document.forms["post_detail"].submit()
    </script>
""".format(post_id=post_id, time=time, message=message, current_user=current_user, zid=zid)




def new_reply_field(parameters):
    print(page_header())
    print(navigation(parameters))
    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('zid')
    from_zid_comment = parameters.getvalue('from_zid_comment')
    from_zid_comment_name = get_name(from_zid_comment)
    comment = parameters.getvalue('comment')
    time_comment = parameters.getvalue('time_comment')
    comment_id = parameters.getvalue('comment_id')
    post_id = parameters.getvalue('post_id')
    time = parameters.getvalue('time')
    message = parameters.getvalue('message')

    with open(os.path.join('templates', 'reply_field.html')) as file:
        reply_field = file.read()
    return reply_field.format(from_zid_comment_name=from_zid_comment_name, post_id=post_id, time=time, message=message, comment_id=comment_id, comment=comment, current_user=current_user, zid=zid)






def post_detail(parameters):
    print(page_header())
    print(navigation(parameters))
    message = parameters.getvalue('message')
    post_id = parameters.getvalue('post_id')
    time = parameters.getvalue('time')
    comment_result = get_comment(post_id) 
    zid = parameters.getvalue('zid')
    current_user = parameters.getvalue('current_user')
    if current_user == zid:
        with open(os.path.join('templates', 'post_detail_current_user.html')) as file:
            comment_template = file.read()
        with open(os.path.join('templates', 'reply_current_user.html')) as file:
            reply_template = file.read()
    else:
        with open(os.path.join('templates', 'post_detail_others.html')) as file:
            comment_template = file.read()
        with open(os.path.join('templates', 'reply_others.html')) as file:
            reply_template = file.read()

    with open(os.path.join('templates', 'new_comment.html')) as file:
        new_comment = file.read().format(post_id=post_id, time=time, message=message, current_user=current_user, zid=zid)

    commom_header = """
    <section class="container">
    <div class="matelook_comment">
    <div class="child">
        <p>{message}</p>
        <br><br>
        <div class="child">
"""
    commom_tail = """
        </div>
    </div>
</div>
</section>
"""
    comment_part = ''
    for c in comment_result:
        reply_part = ''
        comment_id = c[0]
        from_zid_comment = c[1]
        from_zid_comment_name = get_name(from_zid_comment)
        comment = c[3].encode('ascii', 'ignore').decode('ascii')
        comment = replace_zid_with_name(comment)
        time_comment = c[4].replace('T', ' ')
        time_comment = re.sub(r'\+\d*', '', time_comment)
        reply_result = get_reply(comment_id)
        for r in reply_result:
            reply_id = r[0]
            from_zid_reply = r[1]
            from_zid_reply_name = get_name(from_zid_reply)
            reply = r[3].encode('ascii', 'ignore').decode('ascii')
            reply = replace_zid_with_name(reply)
            time_reply = r[4].replace('T', ' ')
            time_reply = re.sub(r'\+\d*', '', time_reply)
            reply_part += reply_template.format(from_zid_reply=from_zid_reply, from_zid_reply_name=from_zid_reply_name, reply=reply, time_reply=time_reply, reply_id=reply_id, current_user=current_user, post_id=post_id, message=message, time=time, zid=zid)
        comment_part += comment_template.format(from_zid_comment=from_zid_comment, from_zid_comment_name=from_zid_comment_name, comment=comment, time_comment=time_comment, comment_id=comment_id, post_id=post_id, time=time, message=message, current_user=current_user, zid=zid) + reply_part + "</div>"

    return commom_header.format(message=message) + new_comment + "<p>Comment:</p>" + comment_part + commom_tail



def create_account_field(parameters):
    print(page_header())
    with open(os.path.join('templates', 'create_account_field.html')) as file:
        return file.read()


def create_account(parameters):
    print(page_header())
    zid = parameters.getvalue('zid')
    email = parameters.getvalue('email')
    password = parameters.getvalue('password')
    password_again = parameters.getvalue('password_again')
    username = parameters.getvalue('username')
    birthday = parameters.getvalue('birthday')
    home_suburb = parameters.getvalue('home_suburb')
    program = parameters.getvalue('program')
    course = parameters.getvalue('course')

    zid_valid = check_zid_exist(zid)   
    email_valid = check_email_valid(email) 
    password_consistent = check_password(password, password_again)

    if zid_valid and email_valid and password_consistent:
        # print("yes")
        send_email(email)
        sql = "INSERT INTO USER_INFO (ZID, USERNAME, PASSWORD, BIRTHDAY, HOME_SUBURB, PROGRAM, COURSE, EMAIL)\
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        conn = sqlite3.connect('user.db')
        cursor = conn.execute(sql, (zid, username, password, birthday, home_suburb, program, course, email))
        conn.commit()

        os.makedirs('dataset-medium/%s' % zid)
        user_txt = """zid={zid}
email={email}
password={password}
username={username}
birthday={birthday}
home_suburb={home_suburb}
program={program}
course={course}
""".format(zid=zid, email=email, password=password, username=username, birthday=birthday, home_suburb=home_suburb, program=program, course=course)

        file_open = open(os.path.join('dataset-medium', '%s' % zid, 'user.txt'), 'w')
        file_open.write(user_txt)
        file_open.close()

        return """
        <div align="center">
        <p>Please login your email and activate your account</p>
        <form method="POST" action="?url=">
        <input type="submit" value="Go to Index Page">
        </form>
        </div>
        """
    else:
        wrong_in_register = """
        <div align="center">
        <form method="POST" action="?url=create_account_field">
        <p>{message}</p>
        <input type="submit" value="back">
        </form>
        </div>
        """
        if not zid_valid:
            message = "This ZID has been used. Please enter another one."
            return wrong_in_register.format(message=message)
        elif not email_valid:
            message = "The EMALI ADDRESS is not vlaid. Please correct it."
            return wrong_in_register.format(message=message)
        elif not password_consistent:
            message = "PASSWORDS typed in two times are not consistent, please correct it."
            return wrong_in_register.format(message=message)



def update_info_field(parameters):
    print(page_header())
    print(navigation(parameters))
    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('zid')
    sql = "SELECT * FROM USER_INFO WHERE ZID=\'{}\'"
    arguments = [zid]
    cursor = query(sql, arguments)
    original_info = cursor.fetchone()
    username = original_info[1]
    original_password_for_check = original_info[2]
    birthday = original_info[3]
    home_suburb = original_info[4]
    program = original_info[7]
    course = original_info[8]
    email = original_info[10]
    self_intro = original_info[11]
    with open(os.path.join('templates', 'update_info_field.html')) as file:
        return file.read().format(zid=zid, username=username, birthday=birthday, home_suburb=home_suburb, program=program, course=course, 
                                  email=email, original_password_for_check=original_password_for_check, self_intro=self_intro, current_user=current_user)



def update_info(parameters):
    print(page_header())
    print(navigation(parameters))

    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('zid')
    username = parameters.getvalue('username')
    original_password = parameters.getvalue('original_password')
    original_password_for_check = parameters.getvalue('original_password_for_check')
    new_password = parameters.getvalue('new_password')
    new_password_again = parameters.getvalue('new_password_again')
    birthday = parameters.getvalue('birthday')
    home_suburb = parameters.getvalue('home_suburb')
    program = parameters.getvalue('program')
    course = parameters.getvalue('course')
    email = parameters.getvalue('email')
    self_intro = parameters.getvalue('self_intro')

    error_form = """
            <form method="POST" action="?url=update_info_field">
                <a href="javascript:;" onclick="parentNode.submit();">Back to Update</a>
                <input type="hidden" name="zid" value="{zid}">
            </form>
            """
    with open(os.path.join('templates', 'update_result.html')) as file:
        result = file.read()
    # no change on password
    if not original_password and not new_password and not new_password_again:
        #email is valid
        if check_email_valid(email):
            sql = """UPDATE USER_INFO SET USERNAME=?, BIRTHDAY=?, HOME_SUBURB=?, 
                                          PROGRAM=?, COURSE=?, EMAIL=?, DETAIL=? WHERE ZID=?"""
            arguments = [username, birthday, home_suburb, program, course, email, self_intro, zid]
            total_changes = update_database(sql, arguments)
            if total_changes > 0:
                message = "Your information has been updated."
                return result.format(message=message, current_user=current_user)
        else:
            message = "Email address is not valid, please correct it."
            return result.format(message=message, current_user=current_user)
    elif original_password and new_password and new_password_again:
        if original_password == original_password_for_check:
            if check_password(new_password, new_password_again):
                if original_password != new_password:
                    sql = """UPDATE USER_INFO SET USERNAME=?, PASSWORD=?, BIRTHDAY=?, HOME_SUBURB=?, 
                                          PROGRAM=?, COURSE=?, EMAIL=?, DETAIL=? WHERE ZID=?"""
                    arguments = [username, new_password, birthday, home_suburb, program, course, email, self_intro, zid]
                    total_changes = update_database(sql, arguments)
                    if total_changes > 0:
                        message = "Your information has been updated."
                        return result.format(message=message, current_user=current_user)
                else:
                    message = "New password cannot be same as the old one, please enter a different password."
                    return result.format(message=message, current_user=current_user)
            else:
                message = "New passwords typed in two times are not consistent, please correct it."
                return result.format(message=message, current_user=current_user)
        else:
            message = "The original password is not correct, please try again."
            return result.format(message=message, current_user=current_user)


def delete_post_confirm(parameters):
    print(page_header())
    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('current_user')
    post_id = parameters.getvalue('post_id')
    message =parameters.getvalue('message')
    time = parameters.getvalue('time')
    with open(os.path.join('templates', 'delete_post_confirm.html')) as file:
        return file.read().format(zid=zid, post_id=post_id, message=message, time=time, current_user=current_user)



def delete_post(parameters):
    print(page_header())
    current_user = parameters.getvalue('current_user')
    zid = parameters.getvalue('zid')
    post_id = parameters.getvalue('post_id')
    delete_post_from_db(post_id)
    return """
    <form name="user_homepage" method="POST" action="?url=user_homepage">
    <input type="hidden" name="zid" value="{current_user}">
    <input type="hidden" name="current_user" value="{current_user}">
    </form>
    <script TYPE="text/JavaScript">
        document.forms["user_homepage"].submit()
        
    </script>
    """.format(current_user=current_user)




def send_email(email):
    sender = 'test.for.ass2@gmail.com'
    pwd = 'testfor9041'
    recipient = email
    content = 'http://127.0.0.1:2041/matelook.py.cgi'
    message = (
        "From: %s\r\n" % sender
        + "To: %s\r\n" % recipient
        + "Subject: activate your account\r\n" 
        + "\r\n" 
        + content
    )
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, pwd)
        server.sendmail(sender, recipient, message)
        server.quit()
    except:
        pass


def delete_comment_confirm(parameters):
    print(page_header())
    current_user = parameters.getvalue('current_user')
    from_zid_comment_name = parameters.getvalue('from_zid_comment_name')
    time_comment = parameters.getvalue('time_comment')
    comment_id = parameters.getvalue('comment_id')
    comment = parameters.getvalue('comment')
    post_id = parameters.getvalue('post_id')
    message = parameters.getvalue('message')
    time = parameters.getvalue('time')

    with open(os.path.join('templates', 'delete_comment_confirm.html')) as file:
        return file.read().format(from_zid_comment_name=from_zid_comment_name, current_user=current_user, time_comment=time_comment, comment_id=comment_id, comment=comment, post_id=post_id, message=message, time=time)


def delete_comment(parameters):
    print(page_header())
    comment_id = parameters.getvalue('comment_id')
    post_id = parameters.getvalue('post_id')
    current_user = parameters.getvalue('current_user')
    message = parameters.getvalue('message')
    time = parameters.getvalue('time')
    comment = parameters.getvalue('comment')
    time_comment = parameters.getvalue('time_comment')
    delete_comment_from_db(comment_id)

    return """
    <form name="post_detail" method="POST" action="?url=post_detail">
    <input type="hidden" name="post_id" value="{post_id}">
    <input type="hidden" name="message" value="{message}">
    <input type="hidden" name="time" value="{time}">
    <input type="hidden" name="current_user" value="{current_user}">
    <input type="hidden" name="zid" value="{current_user}">
    </form>
    <script TYPE="text/JavaScript">
        document.forms["post_detail"].submit()
    </script>
    """.format(current_user=current_user, post_id=post_id, message=message, time=time)



def delete_reply_confirm(parameters):
    print(page_header())
    current_user = parameters.getvalue('current_user')
    from_zid_reply_name = parameters.getvalue('from_zid_reply_name')
    reply = parameters.getvalue('reply')
    time_reply = parameters.getvalue('time_reply')
    reply_id = parameters.getvalue('reply_id')
    post_id = parameters.getvalue('post_id')
    message = parameters.getvalue('message')
    time = parameters.getvalue('time')

    with open(os.path.join('templates', 'delete_reply_confirm.html')) as file:
        return file.read().format(from_zid_reply_name=from_zid_reply_name, reply=reply, time_reply=time_reply, reply_id=reply_id, current_user=current_user, post_id=post_id, message=message, time=time) 


def delete_reply_from_db(reply_id):
    sql_del_reply = "DELETE FROM REPLY WHERE REPLY_ID=\'{}\'"
    arguments_del_reply = [reply_id]
    delete_reply = delete_from_db(sql_del_reply, arguments_del_reply)


def delete_reply(parameters):
    print(page_header())
    reply_id = parameters.getvalue('reply_id')
    delete_reply_from_db(reply_id)
    post_id = parameters.getvalue('post_id')
    current_user = parameters.getvalue('current_user')
    message = parameters.getvalue('message')
    time = parameters.getvalue('time')

    return """
    <form name="post_detail" method="POST" action="?url=post_detail">
    <input type="hidden" name="post_id" value="{post_id}">
    <input type="hidden" name="message" value="{message}">
    <input type="hidden" name="time" value="{time}">
    <input type="hidden" name="current_user" value="{current_user}">
    <input type="hidden" name="zid" value="{current_user}">
    </form>
    <script TYPE="text/JavaScript">
        document.forms["post_detail"].submit()
        
    </script>
    """.format(current_user=current_user, post_id=post_id, message=message, time=time)


def check_zid_exist(zid):
    sql = "SELECT ZID FROM USER_INFO WHERE ZID=\'{}\'"
    arguments = [zid]
    cursor = query(sql, arguments)
    if len(cursor.fetchall()) == 1:
        return 0
    else:
        return 1


def check_email_valid(email):
    m = re.match(r'[\w_.]+@[\w]+\.[\w]*\.*[\w]+$', email)
    if m:
        return 1
    else:
        return 0

def check_password(password, password_again):
    if password == password_again:
        return 1
    else:
        return 0

#replace the zid in the comment with name
def replace_zid_with_name(message):
    m = re.findall(r'z\d{7}', message)
    if len(m) > 0:
        for id in m:
            name = get_name(id)
            message = re.sub(id, name, message)
    return message

def get_name(zid):
    sql = "SELECT USERNAME FROM USER_INFO WHERE ZID=\'{}\'"
    arguments = [zid]
    cursor = query(sql, arguments)
    return cursor.fetchone()[0]


def delete_from_db(sql, arguments):
    conn = sqlite3.connect('user.db')
    conn.execute(sql.format(*arguments))
    conn.commit()
    return conn.total_changes



def delete_post_from_db(post_id):
    sql = "DELETE FROM POST WHERE POST_ID=\'{}\'"
    arguments = [post_id]
    delete_post = delete_from_db(sql, arguments)

    sql_comment = "SELECT COMMENT_ID FROM COMMENT WHERE TO_POST_ID=\'{}\'"
    arguments_comment = [post_id]
    cursor_comment = query(sql_comment, arguments_comment)
    comment_id_list = cursor_comment.fetchall()

    for c in comment_id_list:
        comment_id = c[0]
        delete_comment_from_db(comment_id)


def delete_comment_from_db(comment_id):    
    sql_reply = "SELECT REPLY_ID FROM REPLY WHERE TO_COMMENT_ID=\'{}\'"
    arguments_reply = [comment_id]
    cursor_reply = query(sql_reply, arguments_reply)
    reply_id_list = cursor_reply.fetchall()

    for r in reply_id_list:
        reply_id = r[0]
        delete_reply_from_db(reply_id)
        
    sql_del_comment = "DELETE FROM COMMENT WHERE COMMENT_ID=\'{}\'"
    arguments_del_comment = [comment_id]
    delete_comment = delete_from_db(sql_del_comment, arguments_del_comment)


def query(sql, arguments):
    conn = sqlite3.connect('user.db')
    cursor = conn.execute(sql.format(*arguments))
    return cursor


def update_database(sql, arguments):
    conn = sqlite3.connect('user.db')
    conn.execute(sql, (*arguments,))
    conn.commit()
    return conn.total_changes
    


def get_comment(post_id):
    sql = "SELECT * FROM COMMENT WHERE TO_POST_ID=\'{}\' ORDER BY TIME"
    arguments = [post_id]
    cursor = query(sql, arguments)
    return cursor.fetchall()

def get_reply(comment_id):
    sql = "SELECT * FROM REPLY WHERE TO_COMMENT_ID=\'{}\' ORDER BY TIME"
    arguments = [comment_id]
    cursor = query(sql, arguments)
    return cursor.fetchall()


def get_comment_count(post_id):
    sql = "SELECT COUNT(*) FROM COMMENT WHERE TO_POST_ID=\'{}\'"
    arguments = [post_id]
    cursor = query(sql, arguments)
    count = cursor.fetchone()[0]
    return count





#
# HTML placed at the top of every page
#
def page_header():
    return """Content-Type: text/html;charset=utf-8
              Set-Cookie:test=test

<!DOCTYPE html>
<html lang="en">
<head>
<title>matelook</title>
<link href="matelook.css" rel="stylesheet">
</head>
<body>
<div class="matelook_heading">
matelook
</div>
"""


#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable debug is set
#
def page_trailer(parameters):
    html = ""
    if debug:
        html += "".join("<!-- %s=%s -->\n" % (p, parameters.getvalue(p)) for p in parameters)
    html += "</body>\n</html>"
    return html

if __name__ == '__main__':
    debug = 1
    main()

