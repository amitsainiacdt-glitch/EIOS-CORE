class EIOSKernel:

    def __init__(self):
        self.modules = {}

    def register(self, name, module):
        self.modules[name] = module

    def get(self, name):
        return self.modules.get(name)

    def has(self, name):
        return name in self.modules

    def list_modules(self):
        return list(self.modules.keys())

    def initialize(self):
        """
        Initialize all registered modules that expose an initialize() method.
        """
        for name, module in self.modules.items():
            if hasattr(module, "initialize"):
                print(f"Initializing {name}...")
                module.initialize()

    def start(self):
        print("=" * 60)
        print("EIOS KERNEL")
        print("=" * 60)

        self.initialize()

        print(f"Modules Loaded : {len(self.modules)}")
        print("Kernel Started")