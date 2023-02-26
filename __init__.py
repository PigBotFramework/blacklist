from pbf import PBF
from utils.RegCmd import RegCmd

_name = "黑白系统"
_version = "1.0.1"
_description = "黑白系统，包括全局屏蔽、违禁词系统"
_author = "xzyStudio"
_cost = 0.00

class blacklist(PBF):
    def __enter__(self):
        return [
            RegCmd(
                name = "加违禁词 ",
                usage = "加违禁词 <违禁词内容>",
                permission = "anyone",
                function = "blacklist@addWeijin",
                description = "添加违禁词",
                mode = "违禁系统",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "删违禁词 ",
                usage = "删违禁词 <违禁词内容>",
                permission = "anyone",
                function = "blacklist@delWeijin",
                description = "删除指定的违禁词",
                mode = "违禁系统",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "删群违禁词 ",
                usage = "删群违禁词 <违禁词内容>",
                permission = "ao",
                function = "blacklist@delQunWeijin",
                description = "删除指定的群聊违禁词",
                mode = "违禁系统",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "全局屏蔽列表",
                usage = "全局屏蔽列表",
                permission = "anyone",
                function = "blacklist@listQuanjing",
                description = "列出被全局屏蔽的人",
                mode = "全局屏蔽",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "删全局屏蔽 ",
                usage = "删全局屏蔽 <要删的qq号>",
                permission = "ro",
                function = "blacklist@deleteQuanjing",
                description = "删除某个被全局屏蔽的人",
                mode = "全局屏蔽",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "加全局屏蔽 ",
                usage = "加全局屏蔽 <要加的qq号> <原因>",
                permission = "ro",
                function = "blacklist@addQuanjing",
                description = "添加某个被全局屏蔽的人",
                mode = "全局屏蔽",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "违禁词垃圾箱",
                usage = "违禁词垃圾箱",
                permission = "owner",
                function = "blacklist@bWj",
                description = "查看违禁词垃圾箱",
                mode = "违禁系统",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "违禁词审查列表",
                usage = "违禁词审查列表",
                permission = "owner",
                function = "blacklist@vWj",
                description = "查看违禁词审核列表",
                mode = "违禁系统",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "违禁词删除列表",
                usage = "违禁词删除列表",
                permission = "owner",
                function = "blacklist@dvWj",
                description = "查看违禁词删除列表",
                mode = "违禁系统",
                hidden = 0,
                type = "command"
            ),
            RegCmd(
                name = "违禁词审查 ",
                usage = "违禁词审查 <ID> <是否通过>",
                permission = "owner",
                function = "blacklist@tWj",
                description = "审核违禁词",
                mode = "违禁系统",
                hidden = 0,
                type = "command"
            )
        ]
        
    def addWeijin(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        message = self.data.args[1]
        
        if self.data.args[-1] == "单群":
            self.mysql.commonx('INSERT INTO `botWeijin` (`content`, `state`, `qn`) VALUES (%s, 0, %s)', (message, self.data.se.get("group_id")))
        else:
            if uid == self.data.botSettings.get('owner'):
                self.mysql.commonx('INSERT INTO `botWeijin` (`content`, `state`) VALUES (%s, 0)', (message))
            else:
                self.mysql.commonx('INSERT INTO `botWeijin` (`content`, `state`, `qn`) VALUES (%s, 1, 0)', (message))
        self.client.msg().raw('[CQ:face,id=54] 插入成功，等待审核！')
        
        refreshFromSql('botWeijin')
        
    def bWj(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        
        vKwList = self.mysql.selectx('SELECT * FROM `botWeijin` WHERE `state`=2')
        message = '[CQ:face,id=151] {0}-违禁词垃圾箱'.format(self.data.botSettings.get('name'))
        for i in vKwList:
            message += '\n[CQ:face,id=54] 违禁词：'+str(i.get('content'))+'\n      ID：'+str(i.get('id'))
        self.client.msg().raw(message)
        
    def vWj(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        
        vKwList = self.mysql.selectx('SELECT * FROM `botWeijin` WHERE `state`=1')
        message = '[CQ:face,id=151] {0}-违禁词审核列表'.format(self.data.botSettings.get('name'))
        for i in vKwList:
            message += '\n[CQ:face,id=54] 违禁词：'+str(i.get('content'))+'\n      ID：'+str(i.get('id'))
        self.client.msg().raw(message)
        
    def dvWj(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        
        vKwList = self.mysql.selectx('SELECT * FROM `botWeijin` WHERE `state`=3')
        message = '[CQ:face,id=151] {0}-违禁词删除列表'.format(self.data.botSettings.get('name'))
        for i in vKwList:
            message += '\n[CQ:face,id=54] 违禁词：'+str(i.get('content'))+'\n      ID：'+str(i.get('id'))
        self.client.msg().raw(message)
        
    def tWj(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        message = self.data.message
        
        message1 = message.split(' ')
        kwid = message1[0]
        iff = message1[1]
        if iff == '通过':
            state = 0
            message = '[CQ:face,id=54] 已通过！'
        else:
            state = 2
            message = '[CQ:face,id=54] 已移至回收站！'
        self.mysql.commonx('UPDATE `botWeijin` SET `state`=%s WHERE `id`=%s', (state, kwid))
        
        self.client.msg().raw(message)
        
        refreshFromSql('botWeijin')
        
    def delWeijin(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        message = self.data.message
        
        if uid == self.data.botSettings.get('owner'):
            sql = 'UPDATE `botWeijin` SET `state`=2 WHERE `content`=%s and `qn`=0'
        else:
            sql = 'UPDATE `botWeijin` SET `state`=3 WHERE `content`=%s and `qn`=0'
        self.mysql.commonx(sql, (message))
        
        self.client.msg().raw('[CQ:face,id=54] 已提交申请，等待审核！')
        
        refreshFromSql('botWeijin')
        
    def delQunWeijin(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        message = self.data.message
        
        self.mysql.commonx('DELETE FROM `botWeijin` WHERE `content`=%s and `qn`!=0', (message))
        
        self.client.msg().raw('[CQ:face,id=54] 已删除！')
        
        refreshFromSql('botWeijin')
    
    def listQuanjing(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        
        message = '[CQ:face,id=189] {0}-全局拉黑列表'.format(self.data.botSettings.get('name'))
        quanjing = self.mysql.selectx("SELECT * FROM `botQuanping`")
        for i in quanjing:
            message += '\n[CQ:face,id=54] 用户：'+str(i.get('qn'))+'\n     原因：'+str(i.get('reason'))
        self.client.msg().raw(message)
        
    def deleteQuanjing(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        message = self.data.message
        
        self.mysql.commonx("DELETE FROM `botQuanping` WHERE `uuid`=%s and `qn`=%s", (self.data.uuid, message))
        
        self.client.msg().raw('[CQ:face,id=54] 删除成功！')
        
        refreshFromSql('globalBanned')
    
    def addQuanjing(self):
        uid = self.data.se.get('user_id')
        gid = self.data.se.get('group_id')
        message = self.data.message
        
        message1 = message.split(' ')
        qn = message1[0]
        reason = message1[1]
        self.mysql.commonx("INSERT INTO `botQuanping` (`qn`, `reason`, `uuid`, `time`) VALUES (%s, %s, %s, %s)", (qn, reason, self.data.uuid, time.time()))
        
        self.client.msg().raw('[CQ:face,id=54] 添加成功！')
        
        refreshFromSql('globalBanned')