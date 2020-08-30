from jinja2 import Environment


class LatexJinja2Environment(Environment):
    def __init__(
        self,
        block_start_string="\\BLOCK{",
        block_end_string="}",
        variable_start_string="\\VAR{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        line_statement_prefix="%-",
        line_comment_prefix="%#",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
        **kwargs
    ):
        super().__init__(
            block_start_string=block_start_string,
            block_end_string=block_end_string,
            variable_start_string=variable_start_string,
            variable_end_string=variable_end_string,
            comment_start_string=comment_start_string,
            comment_end_string=comment_end_string,
            line_statement_prefix=line_statement_prefix,
            line_comment_prefix=line_comment_prefix,
            trim_blocks=trim_blocks,
            lstrip_blocks=lstrip_blocks,
            autoescape=autoescape,
            **kwargs
        )
