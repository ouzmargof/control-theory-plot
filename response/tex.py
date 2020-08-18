class TexTf:
    def __init__(self):
        self.title = r"$\frac{1}{s+1}$"

    
    def get_title(self):
        return self.title


    def tex_poly(self, poly_num):
        power = len(poly_num)
        poly_str = ''
        for c in poly_num:
            power -= 1
            if c == 0:
                continue
            else:
                poly_str += '{}s^{}+'.format(c, power)
        # remove redundant characters
        poly_str = poly_str[:-1]
        poly_str = poly_str.replace('s^0', '')
        poly_str = poly_str.replace('s^1', 's')
        poly_str = poly_str.replace('1s', 's')
        return poly_str


    def update(self, **kwargs):
        num = kwargs['num']
        den = kwargs['den']
        self.title = r'$\frac{{{}}} {{{}}}$'.format(self.tex_poly(num), self.tex_poly(den))