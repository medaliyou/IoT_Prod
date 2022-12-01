from core.SD import SD
from core.context import SD_Context

if __name__ == '__main__':

    print(SD_Context.ctx)
    SD_Context.ctx = SD("abcdefg")
    print(SD_Context.ctx.TAG_SD)

