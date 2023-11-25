import sys
from io import StringIO

async def evaluate(ctx, *, args=None):
	if "murderaxolotl" == ctx.message.author:
		await ctx.message.delete()

		prev = sys.stdout
		sys.stdout = std = StringIO()

		exec(args)

		sys.stdout = prev

		await ctx.send(std.getvalue())

	else:
		full_report = """\#\# Access Violation Report ##
You are not authorized to perform this action and your attempt to do so has been recorded

Violation by: %s
Message contents: %s

<@1063584978081951814>
"""%(ctx.author, ctx.message.content)

		await ctx.send(full_report)