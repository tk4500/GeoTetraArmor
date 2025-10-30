package ovo.yiran.geotetraarmor.items;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;
import ovo.yiran.geotetraarmor.Config;
import se.mickelus.mutil.network.PacketHandler;
import se.mickelus.tetra.data.DataManager;
import se.mickelus.tetra.gui.GuiModuleOffsets;
import se.mickelus.tetra.items.modular.IModularItem;

public class ModularFeetItem extends ModularArmorItem {
    public ModularFeetItem() {
        super(EquipmentSlot.FEET, "modular_feet");
        majorModuleKeys = new String[]{"feet/left", "feet/right"};
        minorModuleKeys = new String[]{"feet/extra"};
        requiredModules = new String[]{"feet/left", "feet/right"};
    }

    public void commonInit(PacketHandler packetHandler) {
        DataManager.instance.synergyData.onReload(() -> this.synergies = DataManager.instance.synergyData.getOrdered("armor/feet"));
        this.honeBase = Config.FeetHoneBase.get();
        this.honeIntegrityMultiplier = Config.FeetHoneMultiplier.get();
    }

    @Override
    public ItemStack getDefaultInstance() {
        ItemStack itemStack = new ItemStack(this);
        IModularItem.putModuleInSlot(itemStack, "feet/left", "armor/feet/left/vanilla", "vanilla_feet_left/iron");
        IModularItem.putModuleInSlot(itemStack, "feet/right", "armor/feet/right/vanilla", "vanilla_feet_right/iron");
        return itemStack;
    }

    @Override
    public GuiModuleOffsets getMajorGuiOffsets(ItemStack itemStack) {
        return new GuiModuleOffsets(-14, 18, 4, 18);
    }

    @Override
    public GuiModuleOffsets getMinorGuiOffsets(ItemStack itemStack) {
        return new GuiModuleOffsets(-14, 0);
    }
}
