package ovo.yiran.geotetraarmor;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import se.mickelus.tetra.effect.ItemEffect;
import se.mickelus.tetra.items.modular.IModularItem;

import java.util.ArrayList;
import java.util.List;

public class ArmorEffectUtil {
    public static int getArmorTotalEffectLevel(LivingEntity entity, ItemEffect effect) {
        int result = 0;
        for (ItemStack armor : entity.getArmorSlots()) {
            if (armor.getItem() instanceof IModularItem item) {
                result += Math.max(0, item.getEffectLevel(armor, effect));
            }
        }
        return result;
    }

    public static float getArmorTotalEffectEfficiency(LivingEntity entity, ItemEffect effect) {
        float result = 0;
        for (ItemStack armor : entity.getArmorSlots()) {
            if (armor.getItem() instanceof IModularItem item) {
                result += Math.max(0, item.getEffectEfficiency(armor, effect));
            }
        }
        return result;
    }

    public static List<ItemStack> getModularArmors(LivingEntity entity) {
        List<ItemStack> result = new ArrayList<>();
        for (ItemStack armor : entity.getArmorSlots()) {
            if (armor.getItem() instanceof IModularItem item) {
                result.add(armor);
            }
        }
        return result;
    }
}
