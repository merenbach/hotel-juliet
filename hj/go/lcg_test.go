package main

import (
	"testing"
)

// TestCoprime tests the comprimality tester.
func TestCoprime(t *testing.T) {
	tables := []struct {
		a        uint
		b        uint
		expected bool
	}{
		{3, 5, true},
		{7, 20, true},
		{14, 15, true},
		{172, 17, true},
		{2, 4, false},
		{2, 22, false},
		{3, 15, false},
		{14, 28, false},
	}
	for _, table := range tables {
		if out := coprime(table.a, table.b); out != table.expected {
			if table.expected {
				t.Errorf("%d and %d were expected to be comprime, but were not", table.a, table.b)
			} else {
				t.Errorf("%d and %d were not expected to be comprime, but were", table.a, table.b)
			}
		}
	}
}

// TestLCG tests the linear congruential generator.
func TestLCG(t *testing.T) {
	// Some sequences for verification borrowed from: <https://www.mi.fu-berlin.de/inf/groups/ag-tech/teaching/2012_SS/L_19540_Modeling_and_Performance_Analysis_with_Simulation/06.pdf>
	tables := []struct {
		m          uint
		a          uint
		c          uint
		seed       uint
		hulldobell bool
		expected   []uint
	}{
		{
			m:          100,
			a:          17,
			c:          43,
			seed:       27,
			hulldobell: false,
			expected:   []uint{27, 2, 77, 52, 27},
		},
		{
			m:          64,
			a:          13,
			c:          0,
			seed:       1,
			hulldobell: false,
			expected:   []uint{1, 13, 41, 21, 17, 29, 57, 37, 33, 45, 9, 53, 49, 61, 25, 5, 1},
		},
		{
			m:          64,
			a:          13,
			c:          0,
			seed:       2,
			hulldobell: false,
			expected:   []uint{2, 26, 18, 42, 34, 58, 50, 10, 2},
		},
		{
			m:          64,
			a:          13,
			c:          0,
			seed:       3,
			hulldobell: false,
			expected:   []uint{3, 39, 59, 63, 51, 23, 43, 47, 35, 7, 27, 31, 19, 55, 11, 15, 3},
		},
		{
			m:          64,
			a:          13,
			c:          0,
			seed:       4,
			hulldobell: false,
			expected:   []uint{4, 52, 36, 20, 4},
		},
	}

	for _, table := range tables {
		lcg := NewLCG(table.m, table.a, table.c, table.seed)
		hulldobell, err := lcg.HullDobell()
		if hulldobell != table.hulldobell {
			if hulldobell {
				t.Errorf("LCG %+v satisfies Hull-Dobell, contrary to expectations", lcg)
			} else {
				t.Errorf("LCG %+v fails Hull-Dobell, contrary to expectations: %s", lcg, err)
			}
		}

		for idx, e := range table.expected {
			if f := lcg.Next(); e != f {
				t.Errorf("expected item %d from LCG %+v to equal %d, but got %d instead", idx, lcg, e, f)
			}
		}
	}
}
