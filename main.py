#!/usr/bin/env python3
"""
Minecraft Mod Builder - Twórca i kompilator modów do Minecrafta
Forge:  1.16.5, 1.18.2, 1.19.2, 1.19.4, 1.20.1–1.20.6, 1.21–1.21.4
Fabric: 1.19.4, 1.20.1–1.20.6, 1.21–1.21.4
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import os
import subprocess
import threading
import urllib.request
import urllib.error
import zipfile
import shutil
import re
import sys
import json
import platform
import tempfile

# gradle-wrapper.jar — ten sam plik bootstrapuje każdą wersję Gradle
WRAPPER_JAR_URL = (
    "https://raw.githubusercontent.com/gradle/gradle/"
    "v8.8.0/gradle/wrapper/gradle-wrapper.jar"
)

# ─── Konfiguracja wersji ────────────────────────────────────────────────────

FORGE_CONFIGS = {
    "1.21.4": {
        "forge_ver": "54.0.24", "java_ver": 21,
        "forge_range": "[54,)", "mc_range": "[1.21.4,1.22)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21.4-54.0.24/forge-1.21.4-54.0.24-mdk.zip",
    },
    "1.21.3": {
        "forge_ver": "53.0.7", "java_ver": 21,
        "forge_range": "[53,)", "mc_range": "[1.21.3,1.21.4)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21.3-53.0.7/forge-1.21.3-53.0.7-mdk.zip",
    },
    "1.21.2": {
        "forge_ver": "52.0.17", "java_ver": 21,
        "forge_range": "[52,)", "mc_range": "[1.21.2,1.21.3)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21.2-52.0.17/forge-1.21.2-52.0.17-mdk.zip",
    },
    "1.21.1": {
        "forge_ver": "51.0.36", "java_ver": 21,
        "forge_range": "[51,)", "mc_range": "[1.21.1,1.22)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21.1-51.0.36/forge-1.21.1-51.0.36-mdk.zip",
    },
    "1.21": {
        "forge_ver": "51.0.33", "java_ver": 21,
        "forge_range": "[51,)", "mc_range": "[1.21,1.21.1)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21-51.0.33/forge-1.21-51.0.33-mdk.zip",
    },
    "1.20.6": {
        "forge_ver": "50.1.0", "java_ver": 21,
        "forge_range": "[50,)", "mc_range": "[1.20.6,1.21)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.6-50.1.0/forge-1.20.6-50.1.0-mdk.zip",
    },
    "1.20.5": {
        "forge_ver": "50.0.23", "java_ver": 21,
        "forge_range": "[50,)", "mc_range": "[1.20.5,1.20.6)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.5-50.0.23/forge-1.20.5-50.0.23-mdk.zip",
    },
    "1.20.4": {
        "forge_ver": "49.0.48", "java_ver": 17,
        "forge_range": "[49,)", "mc_range": "[1.20.4,1.20.5)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.4-49.0.48/forge-1.20.4-49.0.48-mdk.zip",
    },
    "1.20.3": {
        "forge_ver": "49.0.19", "java_ver": 17,
        "forge_range": "[49,)", "mc_range": "[1.20.3,1.20.4)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.3-49.0.19/forge-1.20.3-49.0.19-mdk.zip",
    },
    "1.20.2": {
        "forge_ver": "48.1.0", "java_ver": 17,
        "forge_range": "[48,)", "mc_range": "[1.20.2,1.20.3)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.2-48.1.0/forge-1.20.2-48.1.0-mdk.zip",
    },
    "1.20.1": {
        "forge_ver": "47.3.22", "java_ver": 17,
        "forge_range": "[47,)", "mc_range": "[1.20.1,1.20.2)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.3.22/forge-1.20.1-47.3.22-mdk.zip",
    },
    "1.19.4": {
        "forge_ver": "45.2.23", "java_ver": 17,
        "forge_range": "[45,)", "mc_range": "[1.19.4,1.20)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.2.23/forge-1.19.4-45.2.23-mdk.zip",
    },
    "1.19.2": {
        "forge_ver": "43.3.13", "java_ver": 17,
        "forge_range": "[43,)", "mc_range": "[1.19.2,1.20)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.2-43.3.13/forge-1.19.2-43.3.13-mdk.zip",
    },
    "1.18.2": {
        "forge_ver": "40.2.21", "java_ver": 17,
        "forge_range": "[40,)", "mc_range": "[1.18.2,1.19)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.18.2-40.2.21/forge-1.18.2-40.2.21-mdk.zip",
    },
    "1.16.5": {
        "forge_ver": "36.2.39", "java_ver": 8,
        "forge_range": "[36,)", "mc_range": "[1.16.5,1.17)",
        "mdk_url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.5-36.2.39/forge-1.16.5-36.2.39-mdk.zip",
    },
}

FABRIC_CONFIGS = {
    "1.21.4": {
        "loader": "0.16.9", "api": "0.116.0+1.21.4",
        "loom": "1.8-SNAPSHOT", "java_ver": 21,
        "yarn": "1.21.4+build.1",
    },
    "1.21.3": {
        "loader": "0.16.9", "api": "0.113.0+1.21.3",
        "loom": "1.8-SNAPSHOT", "java_ver": 21,
        "yarn": "1.21.3+build.2",
    },
    "1.21.2": {
        "loader": "0.16.9", "api": "0.111.0+1.21.2",
        "loom": "1.8-SNAPSHOT", "java_ver": 21,
        "yarn": "1.21.2+build.1",
    },
    "1.21.1": {
        "loader": "0.16.9", "api": "0.108.0+1.21.1",
        "loom": "1.7-SNAPSHOT", "java_ver": 21,
        "yarn": "1.21.1+build.3",
    },
    "1.21": {
        "loader": "0.15.11", "api": "0.102.1+1.21",
        "loom": "1.7-SNAPSHOT", "java_ver": 21,
        "yarn": "1.21+build.9",
    },
    "1.20.6": {
        "loader": "0.15.11", "api": "0.100.8+1.20.6",
        "loom": "1.6-SNAPSHOT", "java_ver": 21,
        "yarn": "1.20.6+build.1",
    },
    "1.20.5": {
        "loader": "0.15.11", "api": "0.99.4+1.20.5",
        "loom": "1.6-SNAPSHOT", "java_ver": 21,
        "yarn": "1.20.5+build.1",
    },
    "1.20.4": {
        "loader": "0.15.11", "api": "0.97.0+1.20.4",
        "loom": "1.5-SNAPSHOT", "java_ver": 17,
        "yarn": "1.20.4+build.3",
    },
    "1.20.3": {
        "loader": "0.15.6", "api": "0.91.1+1.20.3",
        "loom": "1.4-SNAPSHOT", "java_ver": 17,
        "yarn": "1.20.3+build.1",
    },
    "1.20.2": {
        "loader": "0.15.6", "api": "0.89.3+1.20.2",
        "loom": "1.4-SNAPSHOT", "java_ver": 17,
        "yarn": "1.20.2+build.4",
    },
    "1.20.1": {
        "loader": "0.15.11", "api": "0.92.2+1.20.1",
        "loom": "1.3-SNAPSHOT", "java_ver": 17,
        "yarn": "1.20.1+build.10",
    },
    "1.19.4": {
        "loader": "0.15.11", "api": "0.87.2+1.19.4",
        "loom": "1.1-SNAPSHOT", "java_ver": 17,
        "yarn": "1.19.4+build.2",
    },
}

# ─── Kolory UI ──────────────────────────────────────────────────────────────

C = {
    "bg":       "#1a1a2e",
    "bg2":      "#16213e",
    "bg3":      "#0f3460",
    "card":     "#1e293b",
    "accent":   "#7c3aed",
    "accent2":  "#a855f7",
    "green":    "#10b981",
    "red":      "#ef4444",
    "yellow":   "#f59e0b",
    "text":     "#e2e8f0",
    "text2":    "#94a3b8",
    "border":   "#334155",
    "input":    "#0f172a",
    "btn":      "#7c3aed",
    "btn_h":    "#6d28d9",
    "btn2":     "#10b981",
    "btn2_h":   "#059669",
}

# ─── Generatory szablonów ───────────────────────────────────────────────────

def make_mod_id(name: str) -> str:
    return re.sub(r"[^a-z0-9_]", "", name.lower().replace(" ", "_"))

def make_class_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", name.title().replace(" ", ""))


def forge_gradle_properties(mc_ver: str, cfg: dict, mod_id: str, mod_name: str,
                             mod_ver: str, author: str, desc: str, group: str) -> str:
    return f"""org.gradle.jvmargs=-Xmx3G
org.gradle.daemon=false

minecraft_version={mc_ver}
forge_version={cfg['forge_ver']}
minecraft_version_range={cfg['mc_range']}
forge_version_range={cfg['forge_range']}

mod_id={mod_id}
mod_name={mod_name}
mod_license=MIT
mod_version={mod_ver}
mod_group_id={group}
mod_authors={author}
mod_description={desc}
"""


def forge_build_gradle_modern(mc_ver: str, java_ver: int = 17) -> str:
    """build.gradle dla Forge 1.18.2+ (Gradle 7/8, ForgeGradle 5+)"""
    v = _ver(mc_ver)
    if v >= (1, 21, 0):
        fg_version = "[6.0,6.2)"
    elif v >= (1, 20, 0):
        fg_version = "[6.0,6.2)"
    else:
        fg_version = "[5.1,6)"
    return f"""plugins {{
    id 'eclipse'
    id 'idea'
    id 'net.minecraftforge.gradle' version '{fg_version}'
}}

version = mod_version
group = mod_group_id

base {{
    archivesName = mod_id
}}

java.toolchain.languageVersion = JavaLanguageVersion.of({java_ver})

println "Java: ${{System.getProperty 'java.version'}}"

minecraft {{
    mappings channel: 'official', version: minecraft_version
    copyIdeResources = true

    runs {{
        configureEach {{
            workingDirectory project.file('run')
            property 'forge.logging.markers', 'REGISTRIES'
            property 'forge.logging.console.level', 'debug'
            mods {{
                "${{mod_id}}" {{
                    source sourceSets.main
                }}
            }}
        }}
        client {{ }}
        server {{ args '--nogui' }}
        data {{
            workingDirectory project.file('run-data')
            args '--mod', mod_id, '--all',
                 '--output', file('src/generated/resources/'),
                 '--existing', file('src/main/resources/')
        }}
    }}
}}

sourceSets.main.resources {{ srcDir 'src/generated/resources' }}

repositories {{ }}

dependencies {{
    minecraft "net.minecraftforge:forge:${{minecraft_version}}-${{forge_version}}"
}}

processResources {{
    var replaceProperties = [
        minecraft_version      : minecraft_version,
        minecraft_version_range: minecraft_version_range,
        forge_version          : forge_version,
        forge_version_range    : forge_version_range,
        mod_id                 : mod_id,
        mod_name               : mod_name,
        mod_license            : mod_license,
        mod_version            : mod_version,
        mod_authors            : mod_authors,
        mod_description        : mod_description,
    ]
    inputs.properties replaceProperties
    filesMatching(['META-INF/mods.toml', 'pack.mcmeta']) {{
        expand replaceProperties
    }}
}}

jar {{
    manifest {{
        attributes([
            'Specification-Title'   : mod_id,
            'Specification-Vendor'  : mod_authors,
            'Specification-Version' : '1',
            'Implementation-Title'  : project.name,
            'Implementation-Version': project.jar.archiveVersion,
            'Implementation-Vendor' : mod_authors,
        ])
    }}
}}

jar.finalizedBy('reobfJar')
"""


def forge_build_gradle_legacy() -> str:
    """build.gradle dla Forge 1.16.5"""
    return """buildscript {
    repositories {
        maven { url = 'https://maven.minecraftforge.net' }
        mavenCentral()
    }
    dependencies {
        classpath group: 'net.minecraftforge.gradle', name: 'ForgeGradle', version: '5.1.+', changing: true
    }
}
apply plugin: 'net.minecraftforge.gradle'
apply plugin: 'eclipse'
apply plugin: 'maven-publish'

version = mod_version
group = mod_group_id
archivesBaseName = mod_id

java.toolchain.languageVersion = JavaLanguageVersion.of(8)

println "Java: ${System.getProperty 'java.version'}"

minecraft {
    mappings channel: 'official', version: minecraft_version

    runs {
        client {
            workingDirectory project.file('run')
            property 'forge.logging.markers', 'REGISTRIES'
            property 'forge.logging.console.level', 'debug'
            mods {
                "${mod_id}" { source sourceSets.main }
            }
        }
        server {
            workingDirectory project.file('run')
            property 'forge.logging.markers', 'REGISTRIES'
            property 'forge.logging.console.level', 'debug'
            mods {
                "${mod_id}" { source sourceSets.main }
            }
        }
    }
}

dependencies {
    minecraft "net.minecraftforge:forge:${minecraft_version}-${forge_version}"
}

processResources {
    def replaceProperties = [
        minecraft_version      : minecraft_version,
        minecraft_version_range: minecraft_version_range,
        forge_version          : forge_version,
        forge_version_range    : forge_version_range,
        mod_id                 : mod_id,
        mod_name               : mod_name,
        mod_license            : mod_license,
        mod_version            : mod_version,
        mod_authors            : mod_authors,
        mod_description        : mod_description,
    ]
    inputs.properties replaceProperties
    filesMatching(['META-INF/mods.toml', 'pack.mcmeta']) {
        expand replaceProperties
    }
}

jar {
    manifest {
        attributes([
            'Specification-Title'     : mod_id,
            'Specification-Vendor'    : mod_authors,
            'Specification-Version'   : '1',
            'Implementation-Title'    : project.name,
            'Implementation-Version'  : project.jar.archiveVersion,
            'Implementation-Vendor'   : mod_authors,
        ])
    }
}

jar.finalizedBy('reobfJar')
"""


def forge_settings_gradle(mod_id: str) -> str:
    return f"""pluginManagement {{
    repositories {{
        gradlePluginPortal()
        maven {{ url = 'https://maven.minecraftforge.net' }}
        maven {{ url = 'https://maven.parchmentmc.org' }}
    }}
}}

plugins {{
    id 'org.gradle.toolchains.foojay-resolver-convention' version '0.8.0'
}}

rootProject.name = '{mod_id}'
"""


def forge_settings_gradle_legacy(mod_id: str) -> str:
    return f"rootProject.name = '{mod_id}'\n"


def forge_mods_toml(mod_id: str, mod_name: str, mod_ver: str, author: str,
                    desc: str, mc_ver: str, cfg: dict) -> str:
    return f"""modLoader="javafml"
loaderVersion="${{forge_version_range}}"
license="MIT"
issueTrackerURL="https://github.com/{author}/{mod_id}/issues"

[[mods]]
    modId="${{mod_id}}"
    version="${{mod_version}}"
    displayName="${{mod_name}}"
    description='''
{desc}
'''
    [[mods.optional.custom]]

[[dependencies.{mod_id}]]
    modId="forge"
    mandatory=true
    versionRange="${{forge_version_range}}"
    ordering="NONE"
    side="BOTH"

[[dependencies.{mod_id}]]
    modId="minecraft"
    mandatory=true
    versionRange="${{minecraft_version_range}}"
    ordering="NONE"
    side="BOTH"
"""


def _ver(mc_ver: str) -> tuple:
    parts = tuple(int(x) for x in mc_ver.split("."))
    return parts + (0,) * (3 - len(parts))


def forge_pack_mcmeta(mc_ver: str) -> str:
    v = _ver(mc_ver)
    if v >= (1, 21, 4):
        pack_format = 46
    elif v >= (1, 21, 3):
        pack_format = 42
    elif v >= (1, 21, 2):
        pack_format = 41
    elif v >= (1, 21, 0):
        pack_format = 34
    elif v >= (1, 20, 5):
        pack_format = 32
    elif v >= (1, 20, 3):
        pack_format = 22
    elif v >= (1, 20, 2):
        pack_format = 18
    elif v >= (1, 20, 0):
        pack_format = 15
    elif v >= (1, 19, 0):
        pack_format = 12
    elif v >= (1, 18, 0):
        pack_format = 8
    else:
        pack_format = 6
    return json.dumps({
        "pack": {
            "description": "Forge Mod Resources",
            "pack_format": pack_format
        }
    }, indent=4) + "\n"


def forge_main_class_modern(package: str, class_name: str, mod_id: str, mod_name: str) -> str:
    return f"""package {package};

import com.mojang.logging.LogUtils;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.slf4j.Logger;

@Mod({class_name}.MODID)
public class {class_name} {{

    public static final String MODID = "{mod_id}";
    private static final Logger LOGGER = LogUtils.getLogger();

    public {class_name}() {{
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
        modEventBus.addListener(this::commonSetup);
        MinecraftForge.EVENT_BUS.register(this);
        LOGGER.info("{mod_name} mod zaladowany!");
    }}

    private void commonSetup(final FMLCommonSetupEvent event) {{
        LOGGER.info("Konfiguracja wspolna {mod_name}...");
    }}
}}
"""


def forge_main_class_legacy(package: str, class_name: str, mod_id: str, mod_name: str) -> str:
    return f"""package {package};

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

@Mod({class_name}.MOD_ID)
public class {class_name} {{

    public static final String MOD_ID = "{mod_id}";
    private static final Logger LOGGER = LogManager.getLogger();

    public {class_name}() {{
        IEventBus modEventBus = FMLJavaModLoadingContext.get().getModEventBus();
        modEventBus.addListener(this::setup);
        MinecraftForge.EVENT_BUS.register(this);
        LOGGER.info("{mod_name} mod zaladowany!");
    }}

    private void setup(final FMLCommonSetupEvent event) {{
        LOGGER.info("Konfiguracja wspolna {mod_name}...");
    }}
}}
"""


def fabric_build_gradle(cfg: dict, group: str, mod_id: str) -> str:
    return f"""plugins {{
    id 'fabric-loom' version '{cfg["loom"]}'
    id 'maven-publish'
}}

version = project.mod_version
group = project.maven_group

base {{
    archivesName = project.archives_base_name
}}

repositories {{
    maven {{ url "https://maven.fabricmc.net/" }}
}}

dependencies {{
    minecraft "com.mojang:minecraft:${{project.minecraft_version}}"
    mappings "net.fabricmc:yarn:${{project.yarn_mappings}}:v2"
    modImplementation "net.fabricmc:fabric-loader:${{project.loader_version}}"
    modImplementation "net.fabricmc.fabric-api:fabric-api:${{project.fabric_version}}"
}}

processResources {{
    inputs.property "version", project.version
    filteringCharset "UTF-8"
    filesMatching("fabric.mod.json") {{
        expand "version": project.version
    }}
}}

java {{
    sourceCompatibility = JavaVersion.VERSION_{cfg['java_ver']}
    targetCompatibility = JavaVersion.VERSION_{cfg['java_ver']}
    toolchain {{
        languageVersion = JavaLanguageVersion.of({cfg['java_ver']})
    }}
    withSourcesJar()
}}

jar {{
    from("LICENSE") {{ rename {{ "${{it}}_${{project.archivesBaseName}}" }} }}
}}
"""


def fabric_gradle_properties(cfg: dict, mc_ver: str, mod_id: str,
                              mod_name: str, mod_ver: str, group: str) -> str:
    return f"""# Fabric
minecraft_version={mc_ver}
yarn_mappings={cfg['yarn']}
loader_version={cfg['loader']}

# Mod
mod_version={mod_ver}
maven_group={group}
archives_base_name={mod_id}

# Dependencies
fabric_version={cfg['api']}
"""


def fabric_settings_gradle(mod_id: str) -> str:
    return f"""pluginManagement {{
    repositories {{
        maven {{
            name = 'Fabric'
            url = 'https://maven.fabricmc.net/'
        }}
        gradlePluginPortal()
    }}
}}

rootProject.name = "{mod_id}"
"""


def fabric_mod_json(mod_id: str, mod_name: str, mod_ver: str, author: str,
                    desc: str, package: str, class_name: str, mc_ver: str) -> str:
    cfg = FABRIC_CONFIGS.get(mc_ver, FABRIC_CONFIGS["1.20.1"])
    return json.dumps({
        "schemaVersion": 1,
        "id": mod_id,
        "version": "${version}",
        "name": mod_name,
        "description": desc,
        "authors": [author],
        "contact": {
            "homepage": f"https://github.com/{author}/{mod_id}",
            "sources": f"https://github.com/{author}/{mod_id}"
        },
        "license": "MIT",
        "icon": "assets/icon.png",
        "environment": "*",
        "entrypoints": {
            "main": [f"{package}.{class_name}"]
        },
        "mixins": [f"{mod_id}.mixins.json"],
        "depends": {
            "fabricloader": f">={cfg['loader']}",
            "fabric-api": "*",
            "minecraft": f"~{mc_ver}",
            "java": f">={cfg['java_ver']}"
        },
        "suggests": {
            "another-mod": "*"
        }
    }, indent=2, ensure_ascii=False) + "\n"


def fabric_mixins_json(mod_id: str, package: str) -> str:
    return json.dumps({
        "required": True,
        "minVersion": "0.8",
        "package": f"{package}.mixin",
        "compatibilityLevel": "JAVA_17",
        "mixins": [],
        "client": [],
        "injectors": {"defaultRequire": 1}
    }, indent=2) + "\n"


def fabric_pack_mcmeta(mc_ver: str) -> str:
    v = _ver(mc_ver)
    if v >= (1, 21, 4):
        pack_format = 46
    elif v >= (1, 21, 3):
        pack_format = 42
    elif v >= (1, 21, 2):
        pack_format = 41
    elif v >= (1, 21, 0):
        pack_format = 34
    elif v >= (1, 20, 5):
        pack_format = 32
    elif v >= (1, 20, 3):
        pack_format = 22
    elif v >= (1, 20, 2):
        pack_format = 18
    elif v >= (1, 20, 0):
        pack_format = 15
    elif v >= (1, 19, 0):
        pack_format = 12
    else:
        pack_format = 9
    return json.dumps({
        "pack": {
            "pack_format": pack_format,
            "description": "Fabric Mod Resources"
        }
    }, indent=4) + "\n"


def fabric_main_class(package: str, class_name: str, mod_id: str, mod_name: str) -> str:
    return f"""package {package};

import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class {class_name} implements ModInitializer {{

    public static final String MOD_ID = "{mod_id}";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {{
        LOGGER.info("{mod_name} mod zaladowany!");
    }}
}}
"""


def download_wrapper_jar(dest_path: str, log_fn) -> bool:
    """Pobiera gradle-wrapper.jar z GitHub Gradle."""
    log_fn("[*] Pobieranie gradle-wrapper.jar...")
    try:
        urllib.request.urlretrieve(WRAPPER_JAR_URL, dest_path)
        size = os.path.getsize(dest_path)
        if size > 10_000:
            log_fn(f"[+] gradle-wrapper.jar gotowe ({size // 1024} KB)")
            return True
        log_fn(f"[!] Pobrany plik jest podejrzanie maly ({size} B)")
        return False
    except Exception as e:
        log_fn(f"[!] Nie mozna pobrac gradle-wrapper.jar: {e}")
        log_fn("    Uruchom recznie w folderze projektu: gradle wrapper")
        return False


def gradle_wrapper_properties(gradle_ver: str) -> str:
    return f"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-{gradle_ver}-bin.zip
networkTimeout=10000
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""


def gradlew_bat() -> str:
    return r"""@rem Gradle startup script for Windows

@if "%DEBUG%"=="" @echo off
@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
@rem This is normally unused
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if %ERRORLEVEL% equ 0 goto execute

echo. 1>&2
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH. 1>&2
echo. 1>&2
exit /b 1

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo. 1>&2
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME% 1>&2
echo. 1>&2
exit /b 1

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar

@rem Execute Gradle
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_BASE_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*

:end
@rem End local scope for the variables with windows NT shell
if %ERRORLEVEL% equ 0 goto mainEnd

:fail
rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /C_ return code!
set EXIT_CODE=%ERRORLEVEL%
if %EXITCODE% neq 0 goto mainEnd

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
exit /b %EXIT_CODE%
"""


def gradlew_sh() -> str:
    return r"""#!/bin/sh
# Gradle startup script for UN*X

# Attempt to set APP_HOME
# Resolve links: $0 may be a link
app_path=$0

# Need this for daisy-chained symlinks.
while
    APP_HOME=${app_path%"${app_path##*/}"}  # leaves a trailing /; empty if no leading path
    [ -h "$app_path" ]
do
    ls=$( ls -ld "$app_path" )
    link=${ls#*' -> '}
    case $link in             #(
        /*)   app_path=$link ;; #(
        # e.g. step up /foo/bar/lol to /foo/bar when link is ../baz
        *)    app_path=$APP_HOME$link ;;
    esac
done

APP_HOME=$( cd "${APP_HOME:-./}" && pwd -P ) || exit

APP_NAME="Gradle"
APP_BASE_NAME=${0##*/}

# Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.
DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

# Use the maximum available, or set MAX_FD != -1 to use that value.
MAX_FD=maximum

warn () {
    echo "$*"
} >&2

die () {
    echo
    echo "$*"
    echo
    exit 1
} >&2

# OS specific support (must be 'true' or 'false').
cygwin=false
msys=false
darwin=false
nonstop=false
case "$( uname )" in                #(
    CYGWIN* )         cygwin=true  ;; #(
    Darwin* )         darwin=true  ;; #(
    MSYS* | MINGW* )  msys=true   ;; #(
    NONSTOP* )        nonstop=true ;;
esac

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

# Determine the Java command to use to start the JVM.
if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        JAVACMD=$JAVA_HOME/jre/sh/java
    else
        JAVACMD=$JAVA_HOME/bin/java
    fi
    if [ ! -x "$JAVACMD" ] ; then
        die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME"
    fi
else
    JAVACMD=java
    which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH."
fi

# Escape application args
save () {
    for i do printf %s\\n "$i" | sed "s/'/'\\\\''/g;1s/^/'/;\$s/\$/' \\\\/" ; done
    echo " "
}
APP_ARGS=$(save "$@")

# Collect all arguments for the java command;
#   * $DEFAULT_JVM_OPTS, $JAVA_OPTS, and $GRADLE_OPTS can contain fragments of
#     shell script including quotes and variable substitutions, so put them in
#     double quotes to make sure that they get re-expanded; and
#   * put everything else in single quotes, so that it doesn't expand.

set -- \
        "-Dorg.gradle.appname=$APP_BASE_NAME" \
        -classpath "$CLASSPATH" \
        org.gradle.wrapper.GradleWrapperMain \
        "$APP_ARGS"

exec "$JAVACMD" $DEFAULT_JVM_OPTS $JAVA_OPTS $GRADLE_OPTS "$@"
"""


# ─── Logika tworzenia projektu ──────────────────────────────────────────────

class ModConfig:
    def __init__(self, mod_name, mod_ver, author, desc, mc_ver, loader,
                 group, out_dir, use_mdk_download):
        self.mod_name = mod_name
        self.mod_id = make_mod_id(mod_name)
        self.class_name = make_class_name(mod_name)
        self.mod_ver = mod_ver
        self.author = author
        self.desc = desc
        self.mc_ver = mc_ver
        self.loader = loader  # "Forge" or "Fabric"
        self.group = group if group else f"com.{self.author.lower()}.{self.mod_id}"
        self.package = self.group
        self.out_dir = out_dir
        self.use_mdk_download = use_mdk_download
        self.project_dir = os.path.join(out_dir, self.mod_name.replace(" ", ""))


def create_forge_project(cfg: ModConfig, log_fn, code_files: dict = None):
    forge_cfg = FORGE_CONFIGS[cfg.mc_ver]
    proj = cfg.project_dir
    is_legacy = cfg.mc_ver == "1.16.5"

    os.makedirs(proj, exist_ok=True)

    if cfg.use_mdk_download:
        log_fn(f"[*] Pobieranie Forge MDK dla {cfg.mc_ver}...")
        mdk_url = forge_cfg["mdk_url"]
        tmp_zip = os.path.join(tempfile.gettempdir(), f"forge-{cfg.mc_ver}-mdk.zip")
        try:
            def progress_hook(count, block_size, total_size):
                if total_size > 0:
                    pct = int(count * block_size * 100 / total_size)
                    log_fn(f"    Pobieranie... {min(pct, 100)}%", overwrite=True)
            urllib.request.urlretrieve(mdk_url, tmp_zip, reporthook=progress_hook)
            log_fn(f"[+] MDK pobrane pomyslnie.")
            log_fn("[*] Rozpakowywanie MDK...")
            with zipfile.ZipFile(tmp_zip, 'r') as z:
                z.extractall(proj)
            # MDK extracts to a subdir — move contents up
            subdirs = [d for d in os.listdir(proj) if os.path.isdir(os.path.join(proj, d))]
            if subdirs:
                subdir = os.path.join(proj, subdirs[0])
                for item in os.listdir(subdir):
                    shutil.move(os.path.join(subdir, item), proj)
                os.rmdir(subdir)
            # Remove MDK example files
            for remove in ["CREDITS.txt", "LICENSE.txt", "README.txt", "changelog.txt"]:
                p = os.path.join(proj, remove)
                if os.path.exists(p):
                    os.remove(p)
            log_fn("[+] MDK rozpakowane.")
        except Exception as e:
            log_fn(f"[!] Blad pobierania MDK: {e}")
            log_fn("[*] Przechodze do trybu offline...")
            cfg.use_mdk_download = False
        finally:
            if os.path.exists(tmp_zip):
                os.remove(tmp_zip)

    if not cfg.use_mdk_download:
        log_fn("[*] Generowanie plikow Gradle...")
        gradle_dir = os.path.join(proj, "gradle", "wrapper")
        os.makedirs(gradle_dir, exist_ok=True)
        v = _ver(cfg.mc_ver)
        if is_legacy:
            gradle_ver = "6.8.3"
        elif v < (1, 20, 0):
            gradle_ver = "7.5.1"
        elif v >= (1, 21, 0):
            gradle_ver = "8.10"
        elif v >= (1, 20, 5):
            gradle_ver = "8.8"
        else:
            gradle_ver = "8.1.1"
        with open(os.path.join(gradle_dir, "gradle-wrapper.properties"), "w") as f:
            f.write(gradle_wrapper_properties(gradle_ver))
        with open(os.path.join(proj, "gradlew"), "w", newline="\n") as f:
            f.write(gradlew_sh())
        with open(os.path.join(proj, "gradlew.bat"), "w", newline="\r\n") as f:
            f.write(gradlew_bat())
        if platform.system() != "Windows":
            os.chmod(os.path.join(proj, "gradlew"), 0o755)
        download_wrapper_jar(os.path.join(gradle_dir, "gradle-wrapper.jar"), log_fn)

    # gradle.properties
    log_fn("[*] Generowanie gradle.properties...")
    with open(os.path.join(proj, "gradle.properties"), "w") as f:
        f.write(forge_gradle_properties(
            cfg.mc_ver, forge_cfg, cfg.mod_id, cfg.mod_name,
            cfg.mod_ver, cfg.author, cfg.desc, cfg.package
        ))

    # build.gradle
    log_fn("[*] Generowanie build.gradle...")
    with open(os.path.join(proj, "build.gradle"), "w") as f:
        f.write(forge_build_gradle_legacy() if is_legacy else forge_build_gradle_modern(cfg.mc_ver, forge_cfg["java_ver"]))

    # settings.gradle
    with open(os.path.join(proj, "settings.gradle"), "w") as f:
        f.write(forge_settings_gradle_legacy(cfg.mod_id) if is_legacy else forge_settings_gradle(cfg.mod_id))

    # Java source
    pkg_path = cfg.package.replace(".", os.sep)
    src_dir = os.path.join(proj, "src", "main", "java", pkg_path)
    os.makedirs(src_dir, exist_ok=True)
    main_fname = f"{cfg.class_name}.java"
    cf = code_files or {}
    if main_fname in cf and cf[main_fname].strip():
        log_fn(f"[*] Uzywam twojego kodu dla {main_fname}")
        with open(os.path.join(src_dir, main_fname), "w", encoding="utf-8") as f:
            f.write(cf[main_fname])
    else:
        gen = forge_main_class_legacy if is_legacy else forge_main_class_modern
        with open(os.path.join(src_dir, main_fname), "w") as f:
            f.write(gen(cfg.package, cfg.class_name, cfg.mod_id, cfg.mod_name))
    for fname, content in cf.items():
        if fname != main_fname and content.strip():
            log_fn(f"[*] Dodaje plik: {fname}")
            with open(os.path.join(src_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

    # Resources
    res_dir = os.path.join(proj, "src", "main", "resources")
    meta_dir = os.path.join(res_dir, "META-INF")
    os.makedirs(meta_dir, exist_ok=True)
    with open(os.path.join(meta_dir, "mods.toml"), "w") as f:
        f.write(forge_mods_toml(cfg.mod_id, cfg.mod_name, cfg.mod_ver,
                                cfg.author, cfg.desc, cfg.mc_ver, forge_cfg))
    with open(os.path.join(res_dir, "pack.mcmeta"), "w") as f:
        f.write(forge_pack_mcmeta(cfg.mc_ver))

    # assets
    assets_dir = os.path.join(res_dir, "assets", cfg.mod_id, "lang")
    os.makedirs(assets_dir, exist_ok=True)
    with open(os.path.join(assets_dir, "en_us.json"), "w") as f:
        json.dump({f"item.{cfg.mod_id}.example": "Example Item"}, f, indent=2)

    log_fn(f"[+] Projekt Forge '{cfg.mod_name}' dla MC {cfg.mc_ver} gotowy!")
    log_fn(f"    Lokalizacja: {proj}")


def create_fabric_project(cfg: ModConfig, log_fn, code_files: dict = None):
    fabric_cfg = FABRIC_CONFIGS[cfg.mc_ver]
    proj = cfg.project_dir

    os.makedirs(proj, exist_ok=True)
    log_fn("[*] Generowanie projektu Fabric...")

    # Gradle wrapper properties
    gradle_ver_map = {
        "1.21.4": "8.10", "1.21.3": "8.10", "1.21.2": "8.10",
        "1.21.1": "8.8",  "1.21":   "8.8",
        "1.20.6": "8.8",  "1.20.5": "8.8",
        "1.20.4": "8.6",  "1.20.3": "8.1.1", "1.20.2": "8.1.1",
        "1.20.1": "8.1.1", "1.19.4": "7.6.1",
    }
    gradle_ver = gradle_ver_map.get(cfg.mc_ver, "8.1.1")
    gradle_dir = os.path.join(proj, "gradle", "wrapper")
    os.makedirs(gradle_dir, exist_ok=True)
    with open(os.path.join(gradle_dir, "gradle-wrapper.properties"), "w") as f:
        f.write(gradle_wrapper_properties(gradle_ver))
    with open(os.path.join(proj, "gradlew"), "w", newline="\n") as f:
        f.write(gradlew_sh())
    with open(os.path.join(proj, "gradlew.bat"), "w", newline="\r\n") as f:
        f.write(gradlew_bat())
    if platform.system() != "Windows":
        os.chmod(os.path.join(proj, "gradlew"), 0o755)
    download_wrapper_jar(os.path.join(gradle_dir, "gradle-wrapper.jar"), log_fn)

    # Build files
    with open(os.path.join(proj, "build.gradle"), "w") as f:
        f.write(fabric_build_gradle(fabric_cfg, cfg.package, cfg.mod_id))
    with open(os.path.join(proj, "gradle.properties"), "w") as f:
        f.write(fabric_gradle_properties(fabric_cfg, cfg.mc_ver, cfg.mod_id,
                                         cfg.mod_name, cfg.mod_ver, cfg.package))
    with open(os.path.join(proj, "settings.gradle"), "w") as f:
        f.write(fabric_settings_gradle(cfg.mod_id))

    # Java source
    pkg_path = cfg.package.replace(".", os.sep)
    src_dir = os.path.join(proj, "src", "main", "java", pkg_path)
    mixin_dir = os.path.join(src_dir, "mixin")
    os.makedirs(mixin_dir, exist_ok=True)
    main_fname = f"{cfg.class_name}.java"
    cf = code_files or {}
    if main_fname in cf and cf[main_fname].strip():
        log_fn(f"[*] Uzywam twojego kodu dla {main_fname}")
        with open(os.path.join(src_dir, main_fname), "w", encoding="utf-8") as f:
            f.write(cf[main_fname])
    else:
        with open(os.path.join(src_dir, main_fname), "w") as f:
            f.write(fabric_main_class(cfg.package, cfg.class_name, cfg.mod_id, cfg.mod_name))
    for fname, content in cf.items():
        if fname != main_fname and content.strip():
            log_fn(f"[*] Dodaje plik: {fname}")
            with open(os.path.join(src_dir, fname), "w", encoding="utf-8") as f:
                f.write(content)

    # Resources
    res_dir = os.path.join(proj, "src", "main", "resources")
    assets_dir = os.path.join(res_dir, "assets", cfg.mod_id)
    lang_dir = os.path.join(assets_dir, "lang")
    os.makedirs(lang_dir, exist_ok=True)
    with open(os.path.join(res_dir, "fabric.mod.json"), "w") as f:
        f.write(fabric_mod_json(cfg.mod_id, cfg.mod_name, cfg.mod_ver,
                                cfg.author, cfg.desc, cfg.package, cfg.class_name, cfg.mc_ver))
    with open(os.path.join(res_dir, f"{cfg.mod_id}.mixins.json"), "w") as f:
        f.write(fabric_mixins_json(cfg.mod_id, cfg.package))
    with open(os.path.join(res_dir, "pack.mcmeta"), "w") as f:
        f.write(fabric_pack_mcmeta(cfg.mc_ver))
    with open(os.path.join(lang_dir, "en_us.json"), "w") as f:
        json.dump({f"item.{cfg.mod_id}.example": "Example Item"}, f, indent=2)

    log_fn(f"[+] Projekt Fabric '{cfg.mod_name}' dla MC {cfg.mc_ver} gotowy!")
    log_fn(f"    Lokalizacja: {proj}")


# ─── GUI ────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minecraft Mod Builder")
        self.resizable(True, True)
        self.minsize(780, 700)
        self.configure(bg=C["bg"])

        self._setup_style()
        self._build_ui()
        self._center_window(800, 760)
        self._on_loader_change()

    def _center_window(self, w, h):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=C["bg"], foreground=C["text"],
                        fieldbackground=C["input"], bordercolor=C["border"],
                        darkcolor=C["bg2"], lightcolor=C["bg2"],
                        troughcolor=C["bg2"], selectbackground=C["accent"],
                        selectforeground=C["text"])
        style.configure("TFrame", background=C["bg"])
        style.configure("Card.TFrame", background=C["card"],
                        relief="flat", borderwidth=1)
        style.configure("TLabel", background=C["bg"], foreground=C["text"],
                        font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=C["bg"], foreground=C["text"],
                        font=("Segoe UI", 20, "bold"))
        style.configure("Sub.TLabel", background=C["bg"], foreground=C["text2"],
                        font=("Segoe UI", 9))
        style.configure("Card.TLabel", background=C["card"], foreground=C["text"],
                        font=("Segoe UI", 10))
        style.configure("H2.TLabel", background=C["card"], foreground=C["text2"],
                        font=("Segoe UI", 9, "bold"))
        style.configure("TEntry", fieldbackground=C["input"], foreground=C["text"],
                        bordercolor=C["border"], insertcolor=C["text"],
                        font=("Segoe UI", 10))
        style.configure("TCombobox", fieldbackground=C["input"], foreground=C["text"],
                        background=C["input"], selectbackground=C["accent"],
                        font=("Segoe UI", 10))
        style.map("TCombobox",
                  fieldbackground=[("readonly", C["input"])],
                  selectbackground=[("readonly", C["input"])],
                  selectforeground=[("readonly", C["text"])])
        style.configure("TCheckbutton", background=C["card"], foreground=C["text"],
                        font=("Segoe UI", 10))
        style.map("TCheckbutton", background=[("active", C["card"])])
        style.configure("TProgressbar", troughcolor=C["bg2"],
                        background=C["accent"], thickness=6)
        style.configure("Accent.TButton",
                        background=C["btn"], foreground="white",
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0, focuscolor="none",
                        padding=(16, 8))
        style.map("Accent.TButton",
                  background=[("active", C["btn_h"]), ("disabled", C["border"])],
                  foreground=[("disabled", C["text2"])])
        style.configure("Green.TButton",
                        background=C["btn2"], foreground="white",
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0, focuscolor="none",
                        padding=(16, 8))
        style.map("Green.TButton",
                  background=[("active", C["btn2_h"]), ("disabled", C["border"])],
                  foreground=[("disabled", C["text2"])])
        style.configure("Flat.TButton",
                        background=C["bg3"], foreground=C["text"],
                        font=("Segoe UI", 9),
                        borderwidth=0, focuscolor="none",
                        padding=(8, 6))
        style.map("Flat.TButton",
                  background=[("active", C["border"])])
        style.configure("TNotebook", background=C["bg"], borderwidth=0, tabmargins=[0, 0, 0, 0])
        style.configure("TNotebook.Tab", background=C["bg2"], foreground=C["text2"],
                        padding=(14, 7), font=("Segoe UI", 9))
        style.map("TNotebook.Tab",
                  background=[("selected", C["card"])],
                  foreground=[("selected", C["text"])])
        style.configure("TPanedwindow", background=C["border"])

    def _build_ui(self):
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True, padx=20, pady=16)

        # Header
        hdr = ttk.Frame(root)
        hdr.pack(fill="x", pady=(0, 16))
        ttk.Label(hdr, text="⛏  Minecraft Mod Builder", style="Title.TLabel").pack(side="left")
        ttk.Label(hdr, text="v1.0", style="Sub.TLabel").pack(side="left", padx=(8, 0), pady=(8, 0))

        # Notebook (Ustawienia | Kod Java)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, pady=(0, 4))

        tab1 = ttk.Frame(self.notebook, style="Card.TFrame", padding=18)
        tab2 = ttk.Frame(self.notebook, style="Card.TFrame", padding=10)
        self.notebook.add(tab1, text="  Ustawienia  ")
        self.notebook.add(tab2, text="  Kod Java  ")
        self._build_code_tab(tab2)

        card = tab1
        card.columnconfigure(1, weight=1)

        def row(parent, r, label, widget_fn, **kw):
            ttk.Label(parent, text=label, style="H2.TLabel").grid(
                row=r, column=0, sticky="w", padx=(0, 12), pady=5)
            w = widget_fn(parent, **kw)
            w.grid(row=r, column=1, sticky="ew", pady=5)
            return w

        def entry(parent, textvariable=None, **kw):
            e = ttk.Entry(parent, textvariable=textvariable, **kw)
            return e

        # Fields
        self.v_name    = tk.StringVar(value="MyMod")
        self.v_modid   = tk.StringVar()
        self.v_ver     = tk.StringVar(value="1.0.0")
        self.v_author  = tk.StringVar(value="Author")
        self.v_desc    = tk.StringVar(value="Moj pierwszy mod do Minecrafta")
        self.v_group   = tk.StringVar()
        self.v_loader  = tk.StringVar(value="Forge")
        self.v_mcver   = tk.StringVar()
        self.v_outdir  = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        self.v_dl_mdk  = tk.BooleanVar(value=True)

        self.v_name.trace_add("write", self._on_name_change)

        row(card, 0, "Nazwa moda:",
            lambda p, **k: entry(p, textvariable=self.v_name, **k))
        row(card, 1, "Mod ID (auto):",
            lambda p, **k: entry(p, textvariable=self.v_modid, state="readonly", **k))
        row(card, 2, "Wersja moda:",
            lambda p, **k: entry(p, textvariable=self.v_ver, **k))
        row(card, 3, "Autor:",
            lambda p, **k: entry(p, textvariable=self.v_author, **k))
        row(card, 4, "Opis:",
            lambda p, **k: entry(p, textvariable=self.v_desc, **k))
        row(card, 5, "Pakiet (group):",
            lambda p, **k: entry(p, textvariable=self.v_group,
                                 foreground=C["text2"], **k))

        ttk.Separator(card, orient="horizontal").grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=10)

        # Loader selector
        ttk.Label(card, text="Mod Loader:", style="H2.TLabel").grid(
            row=7, column=0, sticky="w", padx=(0, 12), pady=5)
        lf = ttk.Frame(card, style="Card.TFrame")
        lf.grid(row=7, column=1, sticky="w", pady=5)
        for i, loader in enumerate(["Forge", "Fabric"]):
            ttk.Radiobutton(lf, text=loader, variable=self.v_loader, value=loader,
                            style="TCheckbutton", command=self._on_loader_change
                            ).pack(side="left", padx=(0, 12))

        # MC version
        ttk.Label(card, text="Wersja Minecraft:", style="H2.TLabel").grid(
            row=8, column=0, sticky="w", padx=(0, 12), pady=5)
        self.cb_mcver = ttk.Combobox(card, textvariable=self.v_mcver,
                                     state="readonly", font=("Segoe UI", 10))
        self.cb_mcver.grid(row=8, column=1, sticky="w", pady=5, ipadx=30)

        # Download MDK option (Forge only)
        self.frm_mdk = ttk.Frame(card, style="Card.TFrame")
        self.frm_mdk.grid(row=9, column=0, columnspan=2, sticky="w", pady=2)
        self.chk_mdk = ttk.Checkbutton(self.frm_mdk,
                                        text="Pobierz oficjalny Forge MDK (zalecane, wymaga internetu)",
                                        variable=self.v_dl_mdk,
                                        style="TCheckbutton")
        self.chk_mdk.pack(side="left")

        ttk.Separator(card, orient="horizontal").grid(
            row=10, column=0, columnspan=2, sticky="ew", pady=10)

        # Output dir
        ttk.Label(card, text="Folder wyjsciowy:", style="H2.TLabel").grid(
            row=11, column=0, sticky="w", padx=(0, 12), pady=5)
        dir_frame = ttk.Frame(card, style="Card.TFrame")
        dir_frame.grid(row=11, column=1, sticky="ew", pady=5)
        dir_frame.columnconfigure(0, weight=1)
        ttk.Entry(dir_frame, textvariable=self.v_outdir).grid(
            row=0, column=0, sticky="ew")
        ttk.Button(dir_frame, text="Przeglądaj...", style="Flat.TButton",
                   command=self._browse_dir).grid(row=0, column=1, padx=(6, 0))

        # Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", pady=(16, 8))
        self.btn_create = ttk.Button(btn_frame, text="Utwórz Strukturę",
                                     style="Accent.TButton",
                                     command=self._start_create)
        self.btn_create.pack(side="left", padx=(0, 8))
        self.btn_build = ttk.Button(btn_frame, text="Kompiluj Moda",
                                    style="Green.TButton",
                                    command=self._start_build,
                                    state="disabled")
        self.btn_build.pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="Otwórz Folder",
                   style="Flat.TButton",
                   command=self._open_folder).pack(side="left", padx=(0, 8))
        ttk.Button(btn_frame, text="Wyczyść Log",
                   style="Flat.TButton",
                   command=self._clear_log).pack(side="right")

        # Progress bar
        self.progress = ttk.Progressbar(root, mode="indeterminate",
                                        style="TProgressbar")
        self.progress.pack(fill="x", pady=(0, 8))

        # Log area
        log_frame = ttk.Frame(root, style="Card.TFrame")
        log_frame.pack(fill="both", expand=True)
        ttk.Label(log_frame, text="Log:", style="H2.TLabel",
                  background=C["card"]).pack(anchor="w", padx=8, pady=(6, 2))
        self.log = scrolledtext.ScrolledText(
            log_frame, bg=C["input"], fg=C["text"],
            insertbackground=C["text"], font=("Consolas", 9),
            wrap="word", relief="flat", state="disabled",
            height=12)
        self.log.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.log.tag_configure("ok",   foreground=C["green"])
        self.log.tag_configure("err",  foreground=C["red"])
        self.log.tag_configure("warn", foreground=C["yellow"])
        self.log.tag_configure("info", foreground=C["text2"])

        self._on_name_change()

    # ── Zakładka Kod Java ────────────────────────────────────────────────────

    def _build_code_tab(self, parent):
        self.code_files: dict[str, str] = {}   # {filename: content}
        self._current_cf = None                 # currently shown filename

        info = ttk.Label(parent,
            text="Wklej lub zaimportuj pliki .java. Plik o nazwie pasującej do klasy głównej "
                 "zastąpi szablon. Pozostałe pliki trafią do tego samego pakietu.",
            style="Sub.TLabel", wraplength=740, justify="left")
        info.pack(fill="x", pady=(0, 8))

        paned = tk.PanedWindow(parent, orient="horizontal",
                               bg=C["border"], sashwidth=4,
                               sashrelief="flat", showhandle=False)
        paned.pack(fill="both", expand=True)

        # ── Lewa: lista plików ──────────────────────────────────────────────
        left = ttk.Frame(paned, style="Card.TFrame")
        paned.add(left, width=200, minsize=130)

        ttk.Label(left, text="Pliki projektu:", style="H2.TLabel",
                  background=C["card"]).pack(anchor="w", padx=6, pady=(4, 2))

        lb_frame = ttk.Frame(left, style="Card.TFrame")
        lb_frame.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        sb = tk.Scrollbar(lb_frame, bg=C["bg2"])
        self.cf_listbox = tk.Listbox(
            lb_frame, bg=C["input"], fg=C["text"], selectbackground=C["accent"],
            selectforeground="white", relief="flat", borderwidth=0,
            font=("Consolas", 9), activestyle="none", yscrollcommand=sb.set)
        sb.config(command=self.cf_listbox.yview)
        sb.pack(side="right", fill="y")
        self.cf_listbox.pack(fill="both", expand=True)
        self.cf_listbox.bind("<<ListboxSelect>>", self._cf_select)

        btn_row = ttk.Frame(left, style="Card.TFrame")
        btn_row.pack(fill="x", padx=4, pady=(0, 4))
        ttk.Button(btn_row, text="+ Nowy",   style="Flat.TButton",
                   command=self._cf_new).pack(side="left", padx=(0, 2))
        ttk.Button(btn_row, text="Importuj", style="Flat.TButton",
                   command=self._cf_import).pack(side="left", padx=(0, 2))
        ttk.Button(btn_row, text="Usuń",     style="Flat.TButton",
                   command=self._cf_remove).pack(side="left")

        # ── Prawa: edytor ───────────────────────────────────────────────────
        right = ttk.Frame(paned, style="Card.TFrame")
        paned.add(right, minsize=300)

        self.cf_label = ttk.Label(right, text="(brak wybranego pliku)",
                                  style="H2.TLabel", background=C["card"])
        self.cf_label.pack(anchor="w", padx=6, pady=(4, 2))

        self.cf_editor = scrolledtext.ScrolledText(
            right, bg=C["input"], fg=C["text"],
            insertbackground=C["text"], font=("Consolas", 10),
            wrap="none", relief="flat", state="disabled",
            tabs=("1c",))
        self.cf_editor.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        self.cf_editor.bind("<<Modified>>", self._cf_editor_modified)

    def _cf_select(self, _event=None):
        sel = self.cf_listbox.curselection()
        if not sel:
            return
        # Save current content before switching
        self._cf_save_current()
        name = self.cf_listbox.get(sel[0])
        self._cf_load(name)

    def _cf_load(self, name: str):
        self._current_cf = name
        self.cf_label.config(text=name)
        self.cf_editor.configure(state="normal")
        self.cf_editor.delete("1.0", "end")
        self.cf_editor.insert("1.0", self.code_files.get(name, ""))
        self.cf_editor.edit_modified(False)

    def _cf_save_current(self):
        if self._current_cf is not None:
            self.code_files[self._current_cf] = self.cf_editor.get("1.0", "end-1c")

    def _cf_editor_modified(self, _event=None):
        self.cf_editor.edit_modified(False)
        if self._current_cf:
            self.code_files[self._current_cf] = self.cf_editor.get("1.0", "end-1c")

    def _cf_new(self):
        name = simpledialog.askstring(
            "Nowy plik", "Nazwa pliku .java:",
            initialvalue="MyClass.java", parent=self)
        if not name:
            return
        if not name.endswith(".java"):
            name += ".java"
        self._cf_save_current()
        self.code_files[name] = f"// {name}\n"
        self._cf_refresh_list()
        idx = list(self.code_files.keys()).index(name)
        self.cf_listbox.selection_clear(0, "end")
        self.cf_listbox.selection_set(idx)
        self._cf_load(name)

    def _cf_import(self):
        paths = filedialog.askopenfilenames(
            title="Importuj pliki .java",
            filetypes=[("Java files", "*.java"), ("All files", "*.*")],
            parent=self)
        if not paths:
            return
        self._cf_save_current()
        last = None
        for path in paths:
            name = os.path.basename(path)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    self.code_files[name] = f.read()
                last = name
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie można wczytać {name}:\n{e}", parent=self)
        self._cf_refresh_list()
        if last:
            idx = list(self.code_files.keys()).index(last)
            self.cf_listbox.selection_clear(0, "end")
            self.cf_listbox.selection_set(idx)
            self._cf_load(last)

    def _cf_remove(self):
        sel = self.cf_listbox.curselection()
        if not sel:
            return
        name = self.cf_listbox.get(sel[0])
        del self.code_files[name]
        self._current_cf = None
        self.cf_label.config(text="(brak wybranego pliku)")
        self.cf_editor.configure(state="disabled")
        self.cf_editor.delete("1.0", "end")
        self._cf_refresh_list()

    def _cf_refresh_list(self):
        self.cf_listbox.delete(0, "end")
        for name in self.code_files:
            self.cf_listbox.insert("end", name)

    # ── Eventy ──────────────────────────────────────────────────────────────

    def _on_loader_change(self, *_):
        loader = self.v_loader.get()
        if loader == "Forge":
            versions = list(FORGE_CONFIGS.keys())
            self.frm_mdk.grid()
        else:
            versions = list(FABRIC_CONFIGS.keys())
            self.frm_mdk.grid_remove()
        self.cb_mcver["values"] = versions
        if self.v_mcver.get() not in versions:
            self.v_mcver.set(versions[0])

    def _on_name_change(self, *_):
        mid = make_mod_id(self.v_name.get())
        self.v_modid.set(mid)

    def _browse_dir(self):
        d = filedialog.askdirectory(initialdir=self.v_outdir.get())
        if d:
            self.v_outdir.set(d)

    def _open_folder(self):
        name = self.v_name.get().replace(" ", "")
        proj = os.path.join(self.v_outdir.get(), name)
        if os.path.exists(proj):
            if platform.system() == "Windows":
                os.startfile(proj)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", proj])
            else:
                subprocess.Popen(["xdg-open", proj])
        else:
            messagebox.showinfo("Info", "Folder projektu nie istnieje jeszcze.\nUtwórz najpierw strukturę.")

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    # ── Logowanie ───────────────────────────────────────────────────────────

    _last_was_overwrite = False

    def _log(self, msg: str, overwrite: bool = False):
        self.log.configure(state="normal")
        if overwrite and self._last_was_overwrite:
            self.log.delete("end-2l", "end-1c")
        self._last_was_overwrite = overwrite

        tag = "info"
        if msg.startswith("[+]"):
            tag = "ok"
        elif msg.startswith("[!]"):
            tag = "warn"
        elif msg.startswith("[ERR]") or "FAILED" in msg or "error" in msg.lower():
            tag = "err"

        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.configure(state="disabled")
        self.update_idletasks()

    def _log_safe(self, msg: str, overwrite: bool = False):
        self.after(0, lambda: self._log(msg, overwrite))

    # ── Tworzenie projektu ──────────────────────────────────────────────────

    def _validate(self):
        if not self.v_name.get().strip():
            messagebox.showerror("Błąd", "Podaj nazwę moda!")
            return False
        if not self.v_author.get().strip():
            messagebox.showerror("Błąd", "Podaj nazwę autora!")
            return False
        if not os.path.isdir(self.v_outdir.get()):
            messagebox.showerror("Błąd", "Folder wyjściowy nie istnieje!")
            return False
        return True

    def _build_config(self) -> ModConfig:
        group = self.v_group.get().strip()
        if not group:
            mod_id = make_mod_id(self.v_name.get())
            author_slug = re.sub(r"[^a-z0-9]", "", self.v_author.get().lower())
            group = f"com.{author_slug}.{mod_id}"
        return ModConfig(
            mod_name=self.v_name.get().strip(),
            mod_ver=self.v_ver.get().strip() or "1.0.0",
            author=self.v_author.get().strip(),
            desc=self.v_desc.get().strip(),
            mc_ver=self.v_mcver.get(),
            loader=self.v_loader.get(),
            group=group,
            out_dir=self.v_outdir.get(),
            use_mdk_download=self.v_dl_mdk.get() and self.v_loader.get() == "Forge"
        )

    def _set_busy(self, busy: bool):
        state = "disabled" if busy else "normal"
        self.btn_create.configure(state=state)
        if busy:
            self.progress.start(12)
        else:
            self.progress.stop()
            self.progress["value"] = 0

    def _start_create(self):
        if not self._validate():
            return
        cfg = self._build_config()
        if os.path.exists(cfg.project_dir):
            if not messagebox.askyesno("Uwaga",
                f"Folder '{cfg.project_dir}' już istnieje.\nNadpisać?"):
                return
            shutil.rmtree(cfg.project_dir)

        # Zapisz aktualnie edytowany plik przed startem
        self._cf_save_current()
        code_files = {k: v for k, v in self.code_files.items() if v.strip()}
        if code_files:
            self._log(f"[*] Znaleziono {len(code_files)} plik(ow) kodu uzytkownika: "
                      f"{', '.join(code_files.keys())}")

        self._set_busy(True)
        self._log(f"=== Tworzenie moda: {cfg.mod_name} [{cfg.loader} {cfg.mc_ver}] ===")

        def worker():
            try:
                if cfg.loader == "Forge":
                    create_forge_project(cfg, self._log_safe, code_files)
                else:
                    create_fabric_project(cfg, self._log_safe, code_files)
                self._project_cfg = cfg
                self.after(0, lambda: self.btn_build.configure(state="normal"))
                self._log_safe("=== Gotowe! Mozna teraz skompilowac lub otworzyc folder. ===")
            except Exception as e:
                self._log_safe(f"[ERR] Blad: {e}")
            finally:
                self.after(0, lambda: self._set_busy(False))

        threading.Thread(target=worker, daemon=True).start()

    # ── Kompilacja ──────────────────────────────────────────────────────────

    def _start_build(self):
        if not hasattr(self, "_project_cfg"):
            messagebox.showinfo("Info", "Najpierw utwórz strukturę projektu.")
            return
        cfg: ModConfig = self._project_cfg
        proj = cfg.project_dir
        if not os.path.exists(proj):
            messagebox.showerror("Błąd", f"Folder projektu nie istnieje:\n{proj}")
            return

        gradlew = os.path.join(proj, "gradlew.bat" if platform.system() == "Windows" else "gradlew")
        if not os.path.exists(gradlew):
            messagebox.showerror("Błąd",
                "Brak pliku gradlew!\n"
                "Pobierz Forge MDK lub uruchom:\n"
                "gradle wrapper\n"
                "w folderze projektu.")
            return

        # Spróbuj pobrać gradle-wrapper.jar jeśli brakuje
        jar = os.path.join(proj, "gradle", "wrapper", "gradle-wrapper.jar")
        if not os.path.exists(jar):
            self._log("[!] Brak gradle-wrapper.jar — próbuję pobrać...")
            os.makedirs(os.path.dirname(jar), exist_ok=True)
            if not download_wrapper_jar(jar, self._log):
                messagebox.showerror("Błąd",
                    "Nie udało się pobrać gradle-wrapper.jar.\n"
                    "Sprawdź połączenie z internetem lub uruchom:\n"
                    "gradle wrapper\n"
                    "w folderze projektu.")
                return

        self._set_busy(True)
        self.btn_build.configure(state="disabled")
        self._log("=== Kompilacja moda... ===")
        self._log("[*] To moze zajac kilka minut przy pierwszym uruchomieniu")
        self._log("[*] (Forge/Fabric pobierze zależnosci z internetu)")

        def worker():
            try:
                cmd = [gradlew, "build", "--info"] if platform.system() != "Windows" \
                      else [gradlew, "build", "--info"]
                if platform.system() != "Windows":
                    cmd = ["bash", gradlew, "build"]
                else:
                    cmd = [gradlew, "build"]

                proc = subprocess.Popen(
                    cmd, cwd=proj,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace"
                )
                for line in proc.stdout:
                    line = line.rstrip()
                    if line:
                        self._log_safe(line)
                proc.wait()

                if proc.returncode == 0:
                    build_dir = os.path.join(proj, "build", "libs")
                    jars = [f for f in os.listdir(build_dir) if f.endswith(".jar")
                            and not f.endswith("-sources.jar")] if os.path.exists(build_dir) else []
                    self._log_safe("[+] === KOMPILACJA ZAKONCZONA SUKCESEM! ===")
                    for j in jars:
                        self._log_safe(f"[+] Plik JAR: {os.path.join(build_dir, j)}")
                else:
                    self._log_safe(f"[ERR] Kompilacja nieudana (kod: {proc.returncode})")
            except FileNotFoundError:
                self._log_safe("[ERR] Nie znaleziono gradlew. Sprawdz folder projektu.")
            except Exception as e:
                self._log_safe(f"[ERR] Blad kompilacji: {e}")
            finally:
                self.after(0, lambda: self._set_busy(False))
                self.after(0, lambda: self.btn_build.configure(state="normal"))

        threading.Thread(target=worker, daemon=True).start()


# ─── Start ──────────────────────────────────────────────────────────────────

def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
