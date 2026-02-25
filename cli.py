import argparse
import sys
from bot.client import BinanceClient
from bot.logging_cfg import setup_logging
from bot.validators import validate_order_params
from rich.console import Console
from rich.table import Table

console = Console()
logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot")
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--type", choices=["MARKET", "LIMIT"], help="Required for standard orders")
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--price", type=float, help="Price for LIMIT or TP")
    
    # OCO Arguments
    parser.add_argument("--oco", action="store_true", help="Place OCO (TP/SL) strategy")
    parser.add_argument("--stop_price", type=float, help="Required for OCO (Stop Loss price)")

    args = parser.parse_args()
    bot = BinanceClient()

    try:
        # Handle OCO logic
        if args.oco:
            if not args.price or not args.stop_price:
                console.print("[bold red]Error:[/bold red] OCO requires both --price (TP) and --stop_price (SL).")
                return
            
            logger.info(f"Placing OCO for {args.symbol}")
            response = bot.place_oco_order(args.symbol, args.side, args.qty, args.price, args.stop_price)
            
            console.print(f"[bold green]OCO Orders Placed Successfully![/bold green]")
            console.print(f"Take Profit ID: {response['tp']['orderId']}")
            console.print(f"Stop Loss ID: {response['sl']['orderId']}")

        # Handle Standard Order logic
        else:
            if not args.type:
                console.print("[bold red]Error:[/bold red] --type is required for standard orders.")
                return
                
            validate_order_params(args.type, args.price)
            logger.info(f"Attempting {args.type} {args.side} on {args.symbol}")
            
            response = bot.place_order(args.symbol, args.side, args.type, args.qty, args.price)
            
            logger.info(f"Order Success: {response['orderId']}")
            
            table = Table(title="Order Execution Summary")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("Order ID", str(response.get("orderId")))
            table.add_row("Status", response.get("status"))
            table.add_row("Avg Price", response.get("avgPrice", "N/A"))
            table.add_row("Executed Qty", response.get("executedQty"))
            console.print(table)

    except Exception as e:
        logger.error(f"Execution Failed: {str(e)}")
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
