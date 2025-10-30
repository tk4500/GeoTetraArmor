package ovo.yiran.geotetraarmor.items;

import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;
import ovo.yiran.geotetraarmor.Config;
import se.mickelus.mutil.network.PacketHandler;
import se.mickelus.tetra.data.DataManager;
import se.mickelus.tetra.gui.GuiModuleOffsets;
import se.mickelus.tetra.items.modular.IModularItem;

public class ModularLegsItem extends ModularArmorItem {
    public ModularLegsItem() {
        super(EquipmentSlot.LEGS, "modular_legs");
        majorModuleKeys = new String[]{"legs/left", "legs/right", "legs/belt"};
        minorModuleKeys = new String[]{"legs/extra"};
        requiredModules = new String[]{"legs/left", "legs/right", "legs/belt"};
    }

    public void commonInit(PacketHandler packetHandler) {
        DataManager.instance.synergyData.onReload(() -> this.synergies = DataManager.instance.synergyData.getOrdered("armor/legs"));
        this.honeBase = Config.LegsHoneBase.get();
        this.honeIntegrityMultiplier = Config.LegsHoneMultiplier.get();
    }


    @Override
    public ItemStack getDefaultInstance() {
        ItemStack itemStack = new ItemStack(this);
        IModularItem.putModuleInSlot(itemStack, "legs/belt", "armor/legs/belt/vanilla", "vanilla_legs_belt/iron");
        IModularItem.putModuleInSlot(itemStack, "legs/left", "armor/legs/left/vanilla", "vanilla_legs_left/iron");
        IModularItem.putModuleInSlot(itemStack, "legs/right", "armor/legs/right/vanilla", "vanilla_legs_right/iron");
        return itemStack;
    }

    @Override
    public GuiModuleOffsets getMajorGuiOffsets(ItemStack itemStack) {
        return new GuiModuleOffsets(-21, 13, 11, 13, 4, -2);
    }

    @Override
    public GuiModuleOffsets getMinorGuiOffsets(ItemStack itemStack) {
        return new GuiModuleOffsets(-14,0);
    }
}
