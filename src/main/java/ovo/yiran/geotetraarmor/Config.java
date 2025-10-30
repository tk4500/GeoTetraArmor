package ovo.yiran.geotetraarmor;

import net.minecraftforge.common.ForgeConfigSpec;

public class Config {
    public static final ForgeConfigSpec SPEC;
    private static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();
    public static final ForgeConfigSpec.ConfigValue<Integer> HeadHoneBase;
    public static final ForgeConfigSpec.ConfigValue<Integer> HeadHoneMultiplier;
    public static final ForgeConfigSpec.ConfigValue<Integer> ChestHoneBase;
    public static final ForgeConfigSpec.ConfigValue<Integer> ChestHoneMultiplier;
    public static final ForgeConfigSpec.ConfigValue<Integer> LegsHoneBase;
    public static final ForgeConfigSpec.ConfigValue<Integer> LegsHoneMultiplier;
    public static final ForgeConfigSpec.ConfigValue<Integer> FeetHoneBase;
    public static final ForgeConfigSpec.ConfigValue<Integer> FeetHoneMultiplier;

    static {
        BUILDER.push("HoningConfig");
        HeadHoneBase = BUILDER
                .define("HeadHoneBase", 450);
        HeadHoneMultiplier = BUILDER
                .define("HeadHoneMultiplier", 200);
        ChestHoneBase = BUILDER
                .define("ChestHoneBase", 450);
        ChestHoneMultiplier = BUILDER
                .define("ChestHoneMultiplier", 200);
        LegsHoneBase = BUILDER
                .define("LegsHoneBase", 450);
        LegsHoneMultiplier = BUILDER
                .define("LegsHoneMultiplier", 200);
        FeetHoneBase = BUILDER
                .define("FeetHoneBase", 450);
        FeetHoneMultiplier = BUILDER
                .define("FeetHoneMultiplier", 200);
        BUILDER.pop();
        SPEC = BUILDER.build();
    }
}
