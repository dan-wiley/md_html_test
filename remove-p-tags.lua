function removePTagsInLiBlocksRecursive(blocks)
  for i = 1, #blocks do
    local block = blocks[i]
    if block.tag == "BulletList" or block.tag == "OrderedList" then
      block.content = removePTagsInLiBlocksRecursive(block.content)
    elseif block.tag == "Plain" then
      blocks[i] = pandoc.Span(block.content)
    end
  end
  return blocks
end

function removePTagsInLiBlocks(element)
  if element.tag == "Document" then
    element.blocks = removePTagsInLiBlocksRecursive(element.blocks)
  end
  return element
end

return {
  { Pandoc = removePTagsInLiBlocks }
}
