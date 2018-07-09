from snipssonos.shared.use_case import UseCase
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.exceptions import NoReachableDeviceException


class VolumeUpUseCase(UseCase):
    DEFAULT_VOLUME_INCREMENT = 10

    def __init__(self, device_discovery_service, device_transport_control_service):
        self.device_discovery_service = device_discovery_service
        self.device_transport_control_service = device_transport_control_service

    def process_request(self, request_object):
        devices = self.device_discovery_service.get_devices()

        for device in devices:
            device.increase_volume(self.DEFAULT_VOLUME_INCREMENT)
            self.device_transport_control_service.volume_up(device)

        return ResponseSuccess()
