import React from "react";
import "./styles/problemlist.css"

const blind_75 = [
  {
    name: "Two Sum",
    slug: "two-sum",
    link: "https://leetcode.com/problems/two-sum/",
  },
  {
    name: "Best Time to Buy and Sell Stock",
    slug: "best-time-to-buy-and-sell-stock",
    link: "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
  },
  {
    name: "Contains Duplicate",
    slug: "contains-duplicate",
    link: "https://leetcode.com/problems/contains-duplicate/",
  },
  {
    name: "Product of Array Except Self",
    slug: "product-of-array-except-self",
    link: "https://leetcode.com/problems/product-of-array-except-self/",
  },
  {
    name: "Maximum Subarray",
    slug: "maximum-subarray",
    link: "https://leetcode.com/problems/maximum-subarray/",
  },
  {
    name: "Maximum Product Subarray",
    slug: "maximum-product-subarray",
    link: "https://leetcode.com/problems/maximum-product-subarray/",
  },
  {
    name: "Find Minimum in Rotated Sorted Array",
    slug: "find-minimum-in-rotated-sorted-array",
    link: "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
  },
  {
    name: "Search in Rotated Sorted Array",
    slug: "search-in-rotated-sorted-array",
    link: "https://leetcode.com/problems/search-in-rotated-sorted-array/",
  },
  { name: "3Sum", slug: "3sum", link: "https://leetcode.com/problems/3sum/" },
  {
    name: "Container With Most Water",
    slug: "container-with-most-water",
    link: "https://leetcode.com/problems/container-with-most-water/",
  },
  {
    name: "Climbing Stairs",
    slug: "climbing-stairs",
    link: "https://leetcode.com/problems/climbing-stairs/",
  },
  {
    name: "Set Matrix Zeroes",
    slug: "set-matrix-zeroes",
    link: "https://leetcode.com/problems/set-matrix-zeroes/",
  },
  {
    name: "Group Anagrams",
    slug: "group-anagrams",
    link: "https://leetcode.com/problems/group-anagrams/",
  },
  {
    name: "Maximum Depth of Binary Tree",
    slug: "maximum-depth-of-binary-tree",
    link: "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
  },
  {
    name: "Balanced Binary Tree",
    slug: "balanced-binary-tree",
    link: "https://leetcode.com/problems/balanced-binary-tree/",
  },
  {
    name: "Same Tree",
    slug: "same-tree",
    link: "https://leetcode.com/problems/same-tree/",
  },
  {
    name: "Invert Binary Tree",
    slug: "invert-binary-tree",
    link: "https://leetcode.com/problems/invert-binary-tree/",
  },
  {
    name: "Binary Tree Maximum Path Sum",
    slug: "binary-tree-maximum-path-sum",
    link: "https://leetcode.com/problems/binary-tree-maximum-path-sum/",
  },
  {
    name: "Binary Tree Level Order Traversal",
    slug: "binary-tree-level-order-traversal",
    link: "https://leetcode.com/problems/binary-tree-level-order-traversal/",
  },
  {
    name: "Serialize and Deserialize Binary Tree",
    slug: "serialize-and-deserialize-binary-tree",
    link: "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/",
  },
  {
    name: "Subtree of Another Tree",
    slug: "subtree-of-another-tree",
    link: "https://leetcode.com/problems/subtree-of-another-tree/",
  },
  {
    name: "Construct Binary Tree from Preorder and Inorder Traversal",
    slug: "construct-binary-tree-from-preorder-and-inorder-traversal",
    link: "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/",
  },
  {
    name: "Validate Binary Search Tree",
    slug: "validate-binary-search-tree",
    link: "https://leetcode.com/problems/validate-binary-search-tree/",
  },
  {
    name: "Kth Smallest Element in a BST",
    slug: "kth-smallest-element-in-a-bst",
    link: "https://leetcode.com/problems/kth-smallest-element-in-a-bst/",
  },
  {
    name: "Lowest Common Ancestor of a Binary Search Tree",
    slug: "lowest-common-ancestor-of-a-binary-search-tree",
    link: "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/",
  },
  {
    name: "Implement Trie (Prefix Tree)",
    slug: "implement-trie-prefix-tree",
    link: "https://leetcode.com/problems/implement-trie-prefix-tree/",
  },
  {
    name: "Add and Search Word - Data structure design",
    slug: "add-and-search-word-data-structure-design",
    link: "https://leetcode.com/problems/add-and-search-word-data-structure-design/",
  },
  {
    name: "Word Search",
    slug: "word-search",
    link: "https://leetcode.com/problems/word-search/",
  },
  {
    name: "Combination Sum",
    slug: "combination-sum",
    link: "https://leetcode.com/problems/combination-sum/",
  },
  {
    name: "Combination Sum II",
    slug: "combination-sum-ii",
    link: "https://leetcode.com/problems/combination-sum-ii/",
  },
  {
    name: "First Missing Positive",
    slug: "first-missing-positive",
    link: "https://leetcode.com/problems/first-missing-positive/",
  },
  {
    name: "Trapping Rain Water",
    slug: "trapping-rain-water",
    link: "https://leetcode.com/problems/trapping-rain-water/",
  },
  {
    name: "Jump Game",
    slug: "jump-game",
    link: "https://leetcode.com/problems/jump-game/",
  },
  {
    name: "Coin Change",
    slug: "coin-change",
    link: "https://leetcode.com/problems/coin-change/",
  },
  {
    name: "Longest Increasing Subsequence",
    slug: "longest-increasing-subsequence",
    link: "https://leetcode.com/problems/longest-increasing-subsequence/",
  },
  {
    name: "Unique Paths",
    slug: "unique-paths",
    link: "https://leetcode.com/problems/unique-paths/",
  },
  {
    name: "Minimum Path Sum",
    slug: "minimum-path-sum",
    link: "https://leetcode.com/problems/minimum-path-sum/",
  },
  {
    name: "Edit Distance",
    slug: "edit-distance",
    link: "https://leetcode.com/problems/edit-distance/",
  },
  {
    name: "Word Break",
    slug: "word-break",
    link: "https://leetcode.com/problems/word-break/",
  },
  {
    name: "Merge Intervals",
    slug: "merge-intervals",
    link: "https://leetcode.com/problems/merge-intervals/",
  },
  {
    name: "Insert Interval",
    slug: "insert-interval",
    link: "https://leetcode.com/problems/insert-interval/",
  },
  {
    name: "Non-overlapping Intervals",
    slug: "non-overlapping-intervals",
    link: "https://leetcode.com/problems/non-overlapping-intervals/",
  },
  {
    name: "Meeting Rooms",
    slug: "meeting-rooms",
    link: "https://leetcode.com/problems/meeting-rooms/",
  },
  {
    name: "Meeting Rooms II",
    slug: "meeting-rooms-ii",
    link: "https://leetcode.com/problems/meeting-rooms-ii/",
  },
  {
    name: "Reverse Linked List",
    slug: "reverse-linked-list",
    link: "https://leetcode.com/problems/reverse-linked-list/",
  },
  {
    name: "Linked List Cycle",
    slug: "linked-list-cycle",
    link: "https://leetcode.com/problems/linked-list-cycle/",
  },
  {
    name: "Merge Two Sorted Lists",
    slug: "merge-two-sorted-lists",
    link: "https://leetcode.com/problems/merge-two-sorted-lists/",
  },
  {
    name: "Merge k Sorted Lists",
    slug: "merge-k-sorted-lists",
    link: "https://leetcode.com/problems/merge-k-sorted-lists/",
  },
  {
    name: "Remove Nth Node From End of List",
    slug: "remove-nth-node-from-end-of-list",
    link: "https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
  },
  {
    name: "Reorder List",
    slug: "reorder-list",
    link: "https://leetcode.com/problems/reorder-list/",
  },
  {
    name: "Find the Duplicate Number",
    slug: "find-the-duplicate-number",
    link: "https://leetcode.com/problems/find-the-duplicate-number/",
  },
  {
    name: "Linked List Cycle II",
    slug: "linked-list-cycle-ii",
    link: "https://leetcode.com/problems/linked-list-cycle-ii/",
  },
  {
    name: "Implement Queue using Stacks",
    slug: "implement-queue-using-stacks",
    link: "https://leetcode.com/problems/implement-queue-using-stacks/",
  },
  {
    name: "Implement Stack using Queues",
    slug: "implement-stack-using-queues",
    link: "https://leetcode.com/problems/implement-stack-using-queues/",
  },
  {
    name: "Valid Parentheses",
    slug: "valid-parentheses",
    link: "https://leetcode.com/problems/valid-parentheses/",
  },
  {
    name: "Valid Palindrome",
    slug: "valid-palindrome",
    link: "https://leetcode.com/problems/valid-palindrome/",
  },
  {
    name: "Longest Palindromic Substring",
    slug: "longest-palindromic-substring",
    link: "https://leetcode.com/problems/longest-palindromic-substring/",
  },
  {
    name: "Palindromic Substrings",
    slug: "palindromic-substrings",
    link: "https://leetcode.com/problems/palindromic-substrings/",
  },
  {
    name: "Number of Islands",
    slug: "number-of-islands",
    link: "https://leetcode.com/problems/number-of-islands/",
  },
  {
    name: "Word Ladder",
    slug: "word-ladder",
    link: "https://leetcode.com/problems/word-ladder/",
  },
  {
    name: "Minimum Window Substring",
    slug: "minimum-window-substring",
    link: "https://leetcode.com/problems/minimum-window-substring/",
  },
  {
    name: "Sort Colors",
    slug: "sort-colors",
    link: "https://leetcode.com/problems/sort-colors/",
  },
  {
    name: "Search a 2D Matrix",
    slug: "search-a-2d-matrix",
    link: "https://leetcode.com/problems/search-a-2d-matrix/",
  },
  {
    name: "Find Minimum in Rotated Sorted Array",
    slug: "find-minimum-in-rotated-sorted-array",
    link: "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
  },
  {
    name: "Search in Rotated Sorted Array",
    slug: "search-in-rotated-sorted-array",
    link: "https://leetcode.com/problems/search-in-rotated-sorted-array/",
  },
  {
    name: "Valid Anagram",
    slug: "valid-anagram",
    link: "https://leetcode.com/problems/valid-anagram/",
  },
  {
    name: "Group Anagrams",
    slug: "group-anagrams",
    link: "https://leetcode.com/problems/group-anagrams/",
  },
  {
    name: "Minimum Window Substring",
    slug: "minimum-window-substring",
    link: "https://leetcode.com/problems/minimum-window-substring/",
  },
  {
    name: "Find All Anagrams in a String",
    slug: "find-all-anagrams-in-a-string",
    link: "https://leetcode.com/problems/find-all-anagrams-in-a-string/",
  },
  {
    name: "Longest Substring Without Repeating Characters",
    slug: "longest-substring-without-repeating-characters",
    link: "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
  },
  {
    name: "Longest Repeating Character Replacement",
    slug: "longest-repeating-character-replacement",
    link: "https://leetcode.com/problems/longest-repeating-character-replacement/",
  },
  {
    name: "Minimum Window Substring",
    slug: "minimum-window-substring",
    link: "https://leetcode.com/problems/minimum-window-substring/",
  },
  {
    name: "Sliding Window Maximum",
    slug: "sliding-window-maximum",
    link: "https://leetcode.com/problems/sliding-window-maximum/",
  },
];

const hackerrankQuestions = [
  {"name": "Solve Me First", "link": "https://www.hackerrank.com/challenges/solve-me-first/problem"},
  {"name": "Simple Array Sum", "link": "https://www.hackerrank.com/challenges/simple-array-sum/problem"},
  {"name": "Compare the Triplets", "link": "https://www.hackerrank.com/challenges/compare-the-triplets/problem"},
  {"name": "A Very Big Sum", "link": "https://www.hackerrank.com/challenges/a-very-big-sum/problem"},
  {"name": "Diagonal Difference", "link": "https://www.hackerrank.com/challenges/diagonal-difference/problem"},
  {"name": "Plus Minus", "link": "https://www.hackerrank.com/challenges/plus-minus/problem"},
  {"name": "Staircase", "link": "https://www.hackerrank.com/challenges/staircase/problem"},
  {"name": "Mini-Max Sum", "link": "https://www.hackerrank.com/challenges/mini-max-sum/problem"},
  {"name": "Birthday Cake Candles", "link": "https://www.hackerrank.com/challenges/birthday-cake-candles/problem"},
  {"name": "Time Conversion", "link": "https://www.hackerrank.com/challenges/time-conversion/problem"},
  {"name": "Grading Students", "link": "https://www.hackerrank.com/challenges/grading/problem"},
  {"name": "Apple and Orange", "link": "https://www.hackerrank.com/challenges/apple-and-orange/problem"},
  {"name": "Number Line Jumps", "link": "https://www.hackerrank.com/challenges/kangaroo/problem"},
  {"name": "Between Two Sets", "link": "https://www.hackerrank.com/challenges/between-two-sets/problem"},
  {"name": "Breaking the Records", "link": "https://www.hackerrank.com/challenges/breaking-best-and-worst-records/problem"},
  {"name": "Subarray Division", "link": "https://www.hackerrank.com/challenges/the-birthday-bar/problem"},
  {"name": "Divisible Sum Pairs", "link": "https://www.hackerrank.com/challenges/divisible-sum-pairs/problem"},
  {"name": "Migratory Birds", "link": "https://www.hackerrank.com/challenges/migratory-birds/problem"},
  {"name": "Day of the Programmer", "link": "https://www.hackerrank.com/challenges/day-of-the-programmer/problem"},
  {"name": "Bill Division", "link": "https://www.hackerrank.com/challenges/bon-appetit/problem"}
];


const CodeforcesPracticeProblems = [
    {"name": "Longest Good Array", "link": "https://codeforces.com/problemset/problem/2008/C"},
    {"name": "Dora and C++", "link": "https://codeforces.com/problemset/problem/2007/C"},
    {"name": "osu!mania", "link": "https://codeforces.com/problemset/problem/2009/B"},
    {"name": "Minimize!", "link": "https://codeforces.com/problemset/problem/2009/A"},
    {"name": "Turtle and a MEX Problem (Easy Version)", "link": "https://codeforces.com/problemset/problem/2003/D1"},
    {"name": "Turtle and Good Pairs", "link": "https://codeforces.com/problemset/problem/2003/C"},
    {"name": "Black Circles", "link": "https://codeforces.com/problemset/problem/2002/C"},
    {"name": "Make Three Regions", "link": "https://codeforces.com/problemset/problem/1997/B"},
    {"name": "Even Positions", "link": "https://codeforces.com/problemset/problem/1997/C"},
    {"name": "Sort", "link": "https://codeforces.com/problemset/problem/1996/C"},
    {"name": "Bouquet (Easy Version)", "link": "https://codeforces.com/problemset/problem/1995/B1"},
    {"name": "Bouquet (Hard Version)", "link": "https://codeforces.com/problemset/problem/1995/B2"},
    {"name": "Hungry Games", "link": "https://codeforces.com/problemset/problem/1994/C"},
    {"name": "Light Switches", "link": "https://codeforces.com/problemset/problem/1993/C"},
    {"name": "Parity and Sum", "link": "https://codeforces.com/problemset/problem/1993/B"},
    {"name": "Question Marks", "link": "https://codeforces.com/problemset/problem/1993/A"},
    {"name": "Absolute Zero", "link": "https://codeforces.com/problemset/problem/1991/C"},
    {"name": "AND Reconstruction", "link": "https://codeforces.com/problemset/problem/1991/B"},
    {"name": "Prime XOR Coloring", "link": "https://codeforces.com/problemset/problem/1991/D"},
    {"name": "Mad MAD Sum", "link": "https://codeforces.com/problemset/problem/1990/C"},
    {"name": "Satyam and Counting", "link": "https://codeforces.com/problemset/problem/2009/D"},
    {"name": "Klee's SUPER DUPER LARGE Array!!!", "link": "https://codeforces.com/problemset/problem/2009/E"},
    {"name": "Alternating String", "link": "https://codeforces.com/problemset/problem/2008/E"},
    {"name": "Sakurako's Hobby", "link": "https://codeforces.com/problemset/problem/2008/D"},
    {"name": "Colored Portals", "link": "https://codeforces.com/problemset/problem/2004/D"},
    {"name": "Game with Doors", "link": "https://codeforces.com/problemset/problem/2004/B"},
    {"name": "Closest Point", "link": "https://codeforces.com/problemset/problem/2004/A"},
    {"name": "Call During the Journey", "link": "https://codeforces.com/problemset/problem/2000/G"},
    {"name": "Color Rows and Columns", "link": "https://codeforces.com/problemset/problem/2000/F"},
    {"name": "Photoshoot for Gorillas", "link": "https://codeforces.com/problemset/problem/2000/E"},
    {"name": "Right Left Wrong", "link": "https://codeforces.com/problemset/problem/2000/D"},
    {"name": "Numeric String Template", "link": "https://codeforces.com/problemset/problem/2000/C"},
    {"name": "Ruler (hard version)", "link": "https://codeforces.com/problemset/problem/1999/G2"},
    {"name": "Card Game", "link": "https://codeforces.com/problemset/problem/1999/B"},
    {"name": "Slavic's Exam", "link": "https://codeforces.com/problemset/problem/1999/D"},
    {"name": "Triple Operations", "link": "https://codeforces.com/problemset/problem/1999/E"},
    {"name": "Expected Median", "link": "https://codeforces.com/problemset/problem/1999/F"},
    {"name": "Showering", "link": "https://codeforces.com/problemset/problem/1999/C"},
    {"name": "Perform Operations to Maximize Score", "link": "https://codeforces.com/problemset/problem/1998/C"},
    {"name": "Maximize the Root", "link": "https://codeforces.com/problemset/problem/1997/D"},
    {"name": "Bomb", "link": "https://codeforces.com/problemset/problem/1996/F"},
    {"name": "Squaring", "link": "https://codeforces.com/problemset/problem/1995/C"},
    {"name": "Wooden Game", "link": "https://codeforces.com/problemset/problem/1994/E"},
    {"name": "Funny Game", "link": "https://codeforces.com/problemset/problem/1994/D"},
    {"name": "Fun Game", "link": "https://codeforces.com/problemset/problem/1994/B"},
    {"name": "Diverse Game", "link": "https://codeforces.com/problemset/problem/1994/A"},
    {"name": "Test of Love", "link": "https://codeforces.com/problemset/problem/1992/D"},
    {"name": "Valuable Cards", "link": "https://codeforces.com/problemset/problem/1992/F"},
    {"name": "Array Craft", "link": "https://codeforces.com/problemset/problem/1990/B"},
    {"name": "Smithing Skill", "link": "https://codeforces.com/problemset/problem/1989/D"}
];

const codeLines = [
  "const a = 10;",
  "let b = 20;",
  "function add(x, y) {",
  "  return x + y;",
  "}",
  "console.log(add(a, b));",
  "const c = [1, 2, 3];",
  "c.forEach(num => console.log(num));",
  "const obj = { key: 'value' };",
  "console.log(obj.key);",
];

function Problems() {
  return (
    <div>
      <div className="background-animation">
        {codeLines.map((line, index) => (
          <div key={index} className="code-line">{line}</div>
        ))}
      </div>
      <div className="containerForCode">
        <div className="BooBooBaBa">
          <h1>Blind 75 Problems</h1>
        </div>
        <ul className="problem-list">
          {blind_75.map((problem, index) => (
            <li key={index} className="problem-item">
              <a href={problem.link} className="problem-link lcproblemlink" target="_blank" rel="noopener noreferrer">
                {problem.name}
              </a>
            </li>
          ))}
        </ul>
      </div>


      <div className="containerForCode cfbackground">
        <div className="BooBooBaBa cfheader">
          <h1>Codeforces Practice Problems</h1>
        </div>
        <ul className="problem-list codeforce">
          {CodeforcesPracticeProblems.map((problem, index) => (
            <li key={index} className="problem-item cfproblemitem">
              <a href={problem.link} className="problem-link cflink" target="_blank" rel="noopener noreferrer">
                {problem.name}
              </a>
            </li>
          ))}
        </ul>
      </div>

      <div className="containerForCode hrContainer">
        <div className="BooBooBaBa hrHeader">
          <h1>Hackerrank Problems</h1>
        </div>
        <ul className="problem-list">
          {hackerrankQuestions.map((problem, index) => (
            <li key={index} className="problem-item hrItem">
              <a href={problem.link} className="problem-link hrLink" target="_blank" rel="noopener noreferrer">
                {problem.name}
              </a>
            </li>
          ))}
        </ul>
      </div>


    </div>


  );
}

export default Problems;