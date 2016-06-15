from list import List


class Clean(object):

    class Commands:
        EXITED_CONTAINER = 'docker rm $(docker ps -q -f status=exited)'
        DANGLING_IMAGE = 'docker rmi -f $(docker images -f "dangling=true" -q)'

        ALl_CONTAINER = 'docker rm -f $(docker ps -aq)'
        ALL_IMAGE = 'docker rmi -f $(docker images -q)'

    @classmethod
    def clean(cls):
        images_change_report = List.change_report(cls.Commands.DANGLING_IMAGE, List.Commands.EXITED_IMAGE)
        containers_change_report = List.change_report(cls.Commands.EXITED_CONTAINER, List.Commands.EXITED_CONTAINER)

        return cls._summary(images_change_report, 'dangling images') + cls._summary(
            containers_change_report, 'exited containers')

    @classmethod
    def nuke(cls):
        images_change_report = List.change_report(cls.Commands.ALL_IMAGE, List.Commands.ALL_IMAGE)
        containers_change_report = List.change_report(cls.Commands.ALl_CONTAINER, List.Commands.ALL_CONTAINER)

        return cls._summary(images_change_report, 'images') + cls._summary(containers_change_report, 'containers')

    @classmethod
    def _summary(cls, change_report, obj_name):
        if change_report.start > 0:
            removed = '{} {} removed\n'.format(
                change_report.changed, obj_name)
            remaining = '{} {} remaining\n'.format(
                change_report.end, obj_name)
            return removed + remaining
        else:
            return 'No {} were found.\n'.format(obj_name)

