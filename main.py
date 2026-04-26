from __future__ import annotations

import typer

app = typer.Typer(help="vibe-greet：一个极简、温柔、Agent 友好的问候 CLI。")


@app.command()
def main(
    mood: str = typer.Argument(..., help="今天的心情描述，例如：好累 / 很兴奋 / 有点焦虑"),
    history: bool = typer.Option(False, "--history", help="（阶段 1 预留）查看历史记录"),
) -> None:
    """给出一句基础的 vibe 问候（阶段 1）。"""
    if history:
        typer.echo("阶段 1：--history 功能将在下一阶段实现。")
        raise typer.Exit()

    typer.echo(f"🌅 今天你说“{mood}”，欢迎来到 vibe-greet 的温柔模式！")


if __name__ == "__main__":
    app()
