# Advancement Disabler

Advancement Disabler is a repository for two datapacks that disable all vanilla advancements and recipes for your map and gets rid of all toast messages. Both packs accomplish the same goal, but there are some differences. Select the one that best suits your needs.

You also have the option to **generate these datapacks for any version of Minecraft** by downloading the executable in releases.

- `disable_advancements`
    - This pack invalidates all root advancements by setting an invalid parent.
    - Lightweight and **likely futureproof** but **floods the output log with errors** (they can be ignored).
    - The vanilla advancements will no longer be able to be given via commands.
- `empty_advancements`
    - This pack changes every possible recipe and advancement to be impossible.
    - This pack **must be updated for new advancements in every Minecraft update**.
    - The vanilla advancements will still be able to be given through commands.

## Updated for Minecraft versions 1.15, 1.16, and 1.17

## Visit here to download the datapacks directly: https://github.com/onnowhere/advancement-disabler/releases

## Generating the datapacks yourself from source

This guide is for if you wish to generate these datapacks using the source for any Minecraft version. Note that you can also do this without the following setup by simply running the executable provided in releases.

You will need Python 3.0. This has been tested on Windows.

1. Pull or download the code from the repo.
2. Locate the Minecraft jar for the version you want in `.minecraft/versions`.
3. Double click or run the python file.
4. Drag the Minecraft jar file into the terminal, or paste the file path, and hit enter.
5. The datapacks will be automatically generated and zipped in their respective version folder.

## License

This project is licensed under the CC0 License - see the [LICENSE.md](LICENSE.md) file for details
