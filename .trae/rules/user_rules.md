# 用户规则（user_rules）

1. ANSWER IN CHINESE!
2. `.trae/reference/ref.txt`（如果没有请新建）里面是需要参考的 github 地址或接口文档，如果认为有可参考的内容，在网上搜索（用 agent skill）补充到该文件中。
3. global 参数前置到 py 文件最上边，并且有具体使用位置精确到行的注释。
4. 灵活使用 agent skill 和 mcp 来完成任务。
5. 完成所有任务清单，完成之前不要退出。
6. TDD 模式，每个任务开始前先写测试脚本，测试必须有超时机制，脚本必须通过测试才算完成任务。
7. 将 user_rules.md 文件中的所有规则都保存在：`.trae/rules/user_rules.md` 中。
8. 如果有 git 仓库，先暂存本地修改，然后 `git pull`，然后再继续下面的步骤。
9. 创建 python 便携环境（Miniforge / Micromamba），并安装 requirements.txt 中的包（本次使用 uv）。
10. 每次对话后都要确保 python 的 import 不缺失，requirements.txt 里的模块不缺失；requirements.txt 里面不要写版本号，requirements_{python version}.txt 里面是带版本号的模块。
11. 每次对话后都要 git push to origin:main，commit 内容就是用户说的那句话。
    - user.email="939342547@qq.com"
    - user.name="qq939"
    - remote=https://github.com/qq939/{projectName}
    - branch=main
    - 必要时创建远端仓库：`gh repo create {projectName} --public`
12. `git add .trae/rules/project_rules.md`
13. `git add .trae/rules/user_rules.md`
14. 如果 git 推送到远端失败，rebase 并且 `push --force-with-lease`。
