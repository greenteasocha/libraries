import time
INF = float("inf")
MOD = 998244353


class LazySegmentTree():
    def __init__(self, n, uv, ux, vv, xv, xx, arr=[]):
        self.uv = uv  # unit of val
        self.ux = ux  # unit of lazy
        self.vv = vv  # function (v, v) => v
        self.xv = xv  # function (x, v) => v
        self.xx = xx  # function (x, x) => x

        # define size as power of two
        self.size = 1
        while (n):
            self.size <<= 1
            n //= 2

        self.lv = self.size.bit_length()

        # initialize values
        if arr:
            self._init_arr(arr)
        else:
            self.val = [self.uv()] * (self.size << 1 | 1)
            self.lazy = [self.ux()] * (self.size << 1 | 1)

        return

    def width(self, k):
        return 1 << (self.lv - k.bit_length())

    def _init_arr(self, arr):
        self.val = [self.uv()] * (self.size << 1 | 1)
        for i, val in enumerate(arr):
            self.val[i + self.size] = val
        self.lazy = [self.ux()] * (self.size << 1 | 1)

        self.ascend_all_val()

    def _resolve(self, k):
        # ex.
        # range add => return val + lazy
        # range affine => return val * lazy[0] + lazy[1]
        # ↑ (?)

        # return self.val[k] + self.lazy[k]
        l0, l1 = self.lazy[k] >> 32,  self.lazy[k] % (1 << 32)
        return (self.val[k] * l0 + (l1 << (self.lv - k.bit_length()))) % MOD

    def _get_update_indices(self, l, r):
        # descending order
        l += self.size
        r += self.size - 1
        blen = r.bit_length()
        ret = []

        # lm = (l // (l & -l))
        # rm = (r // (r & -r))

        for i in range(blen + 1):
            # while l:
            # if r <= rm:
            ret.append(r >> i)
            # if l <= lm:
            ret.append(l >> i)

            # l //= 2
            # r //= 2
        return ret

    def _get_update_indices_rev(self, l, r):
        # descending order
        l += self.size
        r += self.size - 1
        blen = r.bit_length()
        ret = []

        for i in range(blen - 1, -1, -1):
            ret.append(r >> i)
            ret.append(l >> i)

        return ret

    def _single_update(self, k):
        if k < self.size:
            l_val = self._resolve(k << 1)
            r_val = self._resolve(k << 1 | 1)

            self.val[k] = self.vv(l_val, r_val)

    def _descend(self, l, r):
        revupdate_indices = self._get_update_indices_rev(l, r)
        for k in revupdate_indices:
            k_val, k_lazy = self.val[k], self.lazy[k]
            self.val[k] = self.xv(k_val, k_lazy, k, self.lv)
            if k < self.size:
                lazy_val = self.lazy[k]

                c_lazy1 = self.lazy[k << 1]
                self.lazy[k << 1] = self.xx(k_lazy, c_lazy1)

                c_lazy2 = self.lazy[k << 1 | 1]
                self.lazy[k << 1 | 1] = self.xx(k_lazy, c_lazy2)

            self.lazy[k] = self.ux()

    def range_query(self, l, r):
        # resolve lazy values in top-down order
        self._descend(l, r)
        # same as default segment tree query
        l += self.size
        r += self.size

        ret = self.uv()
        while l < r:
            if r & 1:
                r -= 1
                ret = self.vv(ret, self._resolve(r))
            if l & 1:
                ret = self.vv(ret, self._resolve(l))
                l += 1

            l >>= 1
            r >>= 1

        return ret

    def range_update(self, l, r, v):
        # resolve lazy values in top-down order
        self._descend(l, r)

        update_indices = self._get_update_indices(l, r)

        # set lazy values
        l += self.size
        r += self.size
        while l < r:
            if r & 1:
                r -= 1
                c_lazy = self.lazy[r]
                self.lazy[r] = self.xx(v, c_lazy)
            if l & 1:
                c_lazy = self.lazy[l]
                self.lazy[l] = self.xx(v, c_lazy)
                l += 1

            l >>= 1
            r >>= 1

        # update real value in bottom-up order
        for k in update_indices:
            if k < self.size:
                # l_val = self._resolve(k << 1)
                l_idx, r_idx = k << 1, k << 1 | 1
                l_val = self.xv(self.val[l_idx],
                                self.lazy[l_idx], l_idx, self.lv)
                # r_val = self._resolve(k << 1 | 1)
                r_val = self.xv(self.val[r_idx],
                                self.lazy[r_idx], r_idx, self.lv)

                self.val[k] = self.vv(l_val, r_val)

    def show_val(self):
        idx = 1
        while idx <= self.size:
            print(self.val[idx:idx << 1])
            idx *= 2

    def show_lazy(self):
        idx = 1
        while idx <= self.size:
            print(self.lazy[idx:idx << 1])
            idx *= 2

    def ascend_all_val(self):
        for i in range(self.size << 1 - 1, -1, -1):
            self._single_update(i)
        return


def main():
    n, m = list(map(int, input().split()))

    def vv(l_val, r_val):
        # (val, val) => val
        return (l_val + r_val) % MOD

    def xv(val, lazy, k, lv):
        # (val, lazy) => val
        l0, l1 = lazy >> 32, lazy % (1 << 32)
        return (val * l0 + (l1 << (lv - k.bit_length()))) % MOD

    def xx(p_lazy, c_lazy):
        # (lazy, lazy) => lazy
        pl0, pl1 = p_lazy >> 32, p_lazy % (1 << 32)
        cl0, cl1 = c_lazy >> 32, c_lazy % (1 << 32)

        r0 = (pl0 * cl0) % MOD
        r1 = (pl0 * cl1 + pl1) % MOD

        return (r0 << 32) + r1

    def uv():
        # initial(unit) value
        return 0

    def ux():
        # initial(unit) lazy
        return 1 << 32

    arr = list(map(int, input().split()))
    st = LazySegmentTree(n, uv, ux, vv, xv, xx, arr)
    sec = time.time()

    ans = []
    for i in range(m):
        q, *param = list(map(int, input().split()))
        if q == 0:
            st.range_update(
                param[0],
                param[1],
                (param[2] << 32) + param[3]
            )
        else:
            v = st.range_query(*param)
            ans.append(v % MOD)

    print(*ans, sep="\n")

    print(time.time() - sec)
    return 0


if __name__ == "__main__":
    main()
