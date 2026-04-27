from __future__ import annotations

import typer

app = typer.Typer(
    help="🍅 vibe-pomo：一个温柔、极简的命令行番茄钟。",
    no_args_is_help=True,
)


@app.command()
def start(
    task: str = typer.Argument(..., help="本次专注任务。"),
    work: int = typer.Option(25, "--work", min=1, help="专注时长（分钟）。"),
    break_time: int = typer.Option(5, "--break-time", min=1, help="休息时长（分钟）。"),
) -> None:
    """开始一个番茄钟（阶段 1：先完成 CLI 命令骨架）。"""
    typer.echo(f"🍅 今日学习任务：{task}")
    typer.echo(f"准备开始：专注 {work} 分钟，休息 {break_time} 分钟。")
    typer.echo("阶段 1 已就绪：下一阶段将加入倒计时与自动记录。")


@app.command()
def today() -> None:
    """查看今日记录（阶段 1 占位）。"""
    typer.echo("today 命令已创建：下一阶段接入真实统计。")


@app.command()
def history() -> None:
    """查看历史记录（阶段 1 占位）。"""
    typer.echo("history 命令已创建：下一阶段接入历史数据。")


@app.command()
def stats() -> None:
    """查看总体统计（阶段 1 占位）。"""
    typer.echo("stats 命令已创建：下一阶段接入累计统计。")


@app.command()
def clear() -> None:
    """清空记录（阶段 1 占位）。"""
    typer.echo("clear 命令已创建：下一阶段加入安全确认。")


if __name__ == "__main__":
    app()
