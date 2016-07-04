from command import Command


class ChangeReport(object):
    def __init__(self, start=0, end=0):
        self.start = start
        self.end = end

    @property
    def changed(self):
        return self.start - self.end

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class List(object):

    class Commands:
        # Docker images: lists images given specified attributes
        # Docker ps: lists containers
        LIVE_IMAGE = 'docker images -f "dangling=false"'
        LIVE_CONTAINER = 'docker ps'

        EXITED_IMAGE = 'docker images -f "dangling=true"'
        EXITED_CONTAINER = 'docker ps -f "status=exited"'

        ALL_IMAGE = 'docker images'
        ALL_CONTAINER = 'docker ps -a'

    @classmethod
    def get_count(cls, command):
        obj_list = Command.call(command, hide_output=True)

        # Subtract 2 for header and footer
        try:
            return len(obj_list.output.split('\n')) - 2
        except AttributeError:
            return 'No count available'

    @classmethod
    def display_list(self, obj_name, list_cmd):
        command_output = Command.call(list_cmd, hide_output=True)

        if command_output.output:
            return '=== {} ===\n{}'.format(obj_name, command_output.output)
        else:
            return 'No {} found'.format(obj_name.lower())

    @classmethod
    def change_report(cls, change_cmd, list_cmd):
        start_num_objs = cls.get_count(list_cmd)

        if start_num_objs > 0:
            Command.call(change_cmd)
            end_num_objs = cls.get_count(list_cmd)

            return ChangeReport(start=start_num_objs, end=end_num_objs)
        else:
            # Default everything is 0
            return ChangeReport()