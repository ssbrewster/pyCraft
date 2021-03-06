import os
import imp

class PluginLoader():
    path = ""
    plugins = {}
    listeners = []

    def __init__(self, path):
        self.path = path

    def loadPlugins(self, parser):
        for item in os.listdir(self.path):
            split = os.path.splitext(item)
            if (split[1] == '.py'):
                name = split[0]
                full_name = split[0].replace(os.path.sep, '.')
                m = imp.load_module(full_name, *imp.find_module(name, [self.path]))

                pluginClass = None
                try:
                    pluginClass = getattr(m, name)()
                    self.plugins[name] = pluginClass
                    try:
                        pluginClass.onEnable(parser, self)
                    except AttributeError:
                        pass
                    try:
                        self.listeners.append(pluginClass.packetReceive)
                    except AttributeError:
                        pass
                except AttributeError:
                    print "Plugin " + name + " is malformed"

    def disablePlugins(self):
        for plugin in self.plugins.values():
            try:
                plugin.onDisable()
            except AttributeError:
                pass

    def notifyOptions(self, options):
        for plugin in self.plugins.values():
            try:
                plugin.optionsParsed(options)
            except AttributeError:
                pass

    def notify(self, methodName):
        for plugin in self.plugins.values():
            try:
                getattr(plugin, methodName)()
            except AttributeError:
                pass

    def getPlugins(self):
        return self.plugins.values()

    def getPlugin(self, name):
        return self.plugins[name]

    def getPacketListeners(self):
        return self.listeners
