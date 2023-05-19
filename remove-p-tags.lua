-- Load the pandoc.lua library
local pandoc = require('pandoc')

-- Function to remove <p> tags from within <li> tags
function removePTagsInLiBlocks (blocks)
  return pandoc.walk_block(pandoc.Div(blocks), {
    Str = function (el)
      return el.content
    end,
    Space = function ()
      return {}
    end
  }).content
end

-- Filter function
function removePTags (doc)
  doc.blocks = removePTagsInLiBlocks(doc.blocks)
  return doc
end

-- Apply the filter
return {
  { Pandoc = removePTags }
}
