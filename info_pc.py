import wmi
import pynvml
from tkinter import *

# pip install pynvml
# pip install WMI

c = wmi.WMI()
pynvml.nvmlInit()


class InformationPC:
    """Get information about the PC"""

    def __init__(self):
        self.cpu = self.get_cpu()
        self.gpu = self.get_gpu()
        self.ram = self.get_ram()
        self.storage = self.get_storage()
        self.bios = self.get_info_bios()
        self.windows = self.get_version_windows()


    def get_cpu(self):
        """Get information about the CPU"""
        cpu = c.Win32_Processor()[0]

        cpu_name = cpu.Name
        cpu_cores = cpu.NumberOfCores
        cpu_brand = cpu.Manufacturer
        cpu_clock_speed = cpu.MaxClockSpeed
        cpu_threads = cpu.NumberOfLogicalProcessors
        cpu_cache_memory = cpu.L2CacheSize
        cpu_socket = cpu.SocketDesignation
        cpu_capacity = cpu.DataWidth
        cpu_architecture = cpu.Architecture
        cpu_family = cpu.Family
        cpu_voltage = cpu.VoltageCaps
        cpu_power = cpu.PowerManagementSupported

        return cpu_name, cpu_cores, cpu_brand, cpu_clock_speed, cpu_threads, cpu_cache_memory, cpu_socket, \
            cpu_capacity, cpu_architecture, cpu_family, cpu_voltage, cpu_power

    def get_gpu(self):
        """Get information about the GPU"""
        gpu = pynvml.nvmlDeviceGetHandleByIndex(0)

        gpu_name = pynvml.nvmlDeviceGetName(gpu).decode('utf-8')
        memory_gpu_info = pynvml.nvmlDeviceGetMemoryInfo(gpu)
        memory_total_gpu = memory_gpu_info.total / 1024 ** 3
        memory_free_gpu = memory_gpu_info.free
        memory_used_gpu = memory_gpu_info.used
        memory_clock = pynvml.nvmlDeviceGetClockInfo(gpu, pynvml.NVML_CLOCK_MEM)
        gpu_clock_speed = pynvml.nvmlDeviceGetClockInfo(gpu, pynvml.NVML_CLOCK_GRAPHICS)
        gpu_boost_clock = pynvml.nvmlDeviceGetMaxClockInfo(gpu, pynvml.NVML_CLOCK_GRAPHICS)
        gpu_temperature = pynvml.nvmlDeviceGetTemperature(gpu, pynvml.NVML_TEMPERATURE_GPU)
        gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(gpu)
        gpu_utilization_gpu = gpu_utilization.gpu
        gpu_utilization_memory = gpu_utilization.memory
        gpu_fan_speed = pynvml.nvmlDeviceGetFanSpeed(gpu)
        gpu_power_usage = pynvml.nvmlDeviceGetPowerUsage(gpu)
        gpu_power_limit = pynvml.nvmlDeviceGetEnforcedPowerLimit(gpu)
        gpu_power_limit_min = pynvml.nvmlDeviceGetPowerManagementLimitConstraints(gpu)[0]
        gpu_power_limit_max = pynvml.nvmlDeviceGetPowerManagementLimitConstraints(gpu)[1]
        gpu_power_limit_default = pynvml.nvmlDeviceGetPowerManagementDefaultLimit(gpu)
        gpu_power_management = pynvml.nvmlDeviceGetPowerManagementMode(gpu)
        driver_version = pynvml.nvmlSystemGetDriverVersion()

        if gpu is None:
            return 'No GPU'
        else:
            return gpu_name, memory_total_gpu, memory_free_gpu, memory_used_gpu, memory_clock, gpu_clock_speed, \
                gpu_boost_clock, gpu_temperature, gpu_utilization_gpu, gpu_utilization_memory, gpu_fan_speed, \
                gpu_power_usage, gpu_power_limit, gpu_power_limit_min, gpu_power_limit_max, gpu_power_limit_default, \
                gpu_power_management, driver_version

    def get_ram(self):
        """Get information about the Memory RAM"""
        ram = c.Win32_PhysicalMemory()[0]

        name_ram = ram.Caption
        ram_capacity = ram.Capacity
        ram_speed = ram.Speed
        ram_voltage = ram.ConfiguredVoltage
        ram_type = ram.MemoryType
        ram_brand = ram.Manufacturer
        ram_form_factor = ram.FormFactor

        return name_ram, ram_capacity, ram_speed, ram_voltage, ram_type, ram_brand, ram_form_factor

    def get_storage(self):
        """Get information about the storage"""
        disk = c.Win32_DiskDrive()[0]
        ssd = c.Win32_LogicalDisk()[0]

        name_disk = disk.Caption
        size_disk = int(disk.Size) / (1024 ** 3)
        size_sdd = int(ssd.Size) / (1024 ** 3)
        disk_model = disk.Model
        disk_media_type = disk.MediaType
        disk_partitions = disk.Partitions

        return name_disk, size_disk, size_sdd, disk_model, disk_media_type, disk_partitions

    def get_info_bios(self):
        """Get information about the BIOS"""
        bios = c.Win32_BIOS()[0]

        bios_name = bios.Name
        bios_version = bios.Version
        bios_release_date = bios.ReleaseDate
        bios_serial_number = bios.SerialNumber
        bios_manufacturer = bios.Manufacturer
        bios_caption = bios.Caption

        return bios_name, bios_version, bios_release_date, bios_serial_number, bios_manufacturer, bios_caption

    def get_version_windows(self):
        """Get information about operational system"""
        win = c.Win32_OperatingSystem()[0]

        win_name = win.Caption
        win_version = win.Version
        win_build_number = win.BuildNumber
        win_install_date = win.InstallDate
        win_local_date_time = win.LocalDateTime
        win_serial_number = win.SerialNumber

        return win_name, win_version, win_build_number, win_install_date, win_local_date_time, win_serial_number

    def get_info_pc(self, text_info=None):
        """Get information about the PC"""
        cpu = self.get_cpu()
        gpu = self.get_gpu()
        ram = self.get_ram()
        storage = self.get_storage()
        bios = self.get_info_bios()
        win = self.get_version_windows()

        text = f'''
               ------------> CPU INFO <------------ 
               CPU: {cpu[0]} 
               Number of cores: {cpu[1]} 
               CPU brand: {cpu[2]} 
               CPU clock speed: {cpu[3]} MHz 
               Number of threads: {cpu[4]} 
               CPU cache memory: {cpu[5]} KB 
               CPU socket: {cpu[6]} 
               CPU capacity: {cpu[7]} bits 
               CPU architecture: {cpu[8]}
               CPU family: {cpu[9]} 
               CPU voltage: {cpu[10]} 
               CPU power management: {cpu[11]} 
               ------------> GPU Info <------------ 
               GPU: {gpu[0]} 
               Memory total GPU: {gpu[1]} GB
               Memory free GPU: {gpu[2]} GB 
               Memory used GPU: {gpu[3]} GB 
               Memory clock: {gpu[4]} MHz 
               GPU clock speed: {gpu[5]} MHz 
               GPU boost clock: {gpu[6]} MHz 
               GPU temperature: {gpu[7]} °C 
               GPU utilization: {gpu[8]} % 
               GPU memory utilization: {gpu[9]} %
               GPU fan speed: {gpu[10]} %
               GPU power usage: {gpu[11]} W 
               GPU power limit: {gpu[12]} W
               GPU power limit min: {gpu[13]} W 
               GPU power limit max: {gpu[14]} W 
               GPU power limit default: {gpu[15]} W 
               GPU power management: {gpu[16]} 
               Driver version: {gpu[17]} 
               ------------> Memory RAM Info <------------ 
               RAM: {ram[0]}
               RAM capacity: {ram[1]} GB 
               RAM speed: {ram[2]} MHz 
               RAM voltage: {ram[3]} V
               RAM type: {ram[4]} 
               RAM brand: {ram[5]} 
               RAM form factor: {ram[6]} 
               ------------> Storage Info <------------ 
               Disk: {storage[0]}
               Disk size: {storage[1]} GB 
               SSD size: {storage[2]} GB
               Disk model: {storage[3]} 
               Disk media type: {storage[4]} 
               Disk partitions: {storage[5]} 
               ------------> BIOS Info <------------ 
               BIOS: {bios[0]} 
               BIOS version: {bios[1]} 
               BIOS release date: {bios[2]} 
               BIOS serial number: {bios[3]} 
               BIOS manufacturer: {bios[4]}
               BIOS caption: {bios[5]} 
               ------------> System Operation Info <------------ 
               Windows: {win[0]} 
               Windows version: {win[1]} 
               Windows build number: {win[2]} 
               Windows install date: {win[3]}
               Windows local date time: {win[4]} 
               Windows serial number: {win[5]} 
               '''

        print(text)

        text_info["text"] = text


class Application(InformationPC):
    """Create a window with information about the PC"""

    def __init__(self):
        super().__init__()
        self.root = Tk()
        #self.root.geometry('300x300')
        self.font = ('Arial', 12)

        # Frame
        self.frame = Frame(self.root)
        self.root.title('Information PC')

        # Label
        self.subtitle = Label(self.frame, text='Information about the PC', font=self.font, fg='#ffffff', bg='#245985')
        self.subtitle.grid(row=0, column=0)

        # Button
        self.button = Button(self.frame, text='Get information', font=self.font, command=self.get_info_pc)
        self.button.grid(row=1, column=0)

        # Text Infos
        self.text_info = Label(self.frame, text=" ", font=self.font)
        self.text_info.grid(row=2, column=0)

        self.frame.pack()
        self.root.mainloop()


def main():
    Application()


if __name__ == '__main__':
    pc = InformationPC()
    main()
